from fastapi import APIRouter, HTTPException, Depends, status
from utils.StorageManager import  StorageManager, get_storage_manager
from utils import helper
from utils.logger import create_logger, log_debug_and_info
import os

LOGGER = create_logger(os.path.basename(__file__))

router = APIRouter(prefix="/manager", tags=["Section"])


@router.post("/section")
def add_section(
    name: str,
    limit:float,
    manager: StorageManager = Depends(get_storage_manager)
    ):
        LOGGER.info("Adding %s section in the database", name)
        if name in manager:
            LOGGER.error("%s already in %s", helper.get_name_parts(name,-1), helper.get_name_parts(name,-2))
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{helper.get_name_parts(name,-1)} already in {helper.get_name_parts(name,-2)}"
            )
        
        maximum_expense_limit = manager.get_propagated_limit_for_child(name)
        if not (manager.get_immidiate_parent_limit(name) >= limit and maximum_expense_limit >= limit):
            LOGGER.error("%s is having more expense than %s cannot add!", helper.get_name_parts(name,-1), helper.get_name_parts(name,-2))
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"{helper.get_name_parts(name,-1)} is having more expense than {helper.get_name_parts(name,-2)} cannot add!"
            )
        manager[name] = {
            "limit": limit,
            "expense":0
        }

        manager.save()
        log_debug_and_info(LOGGER, f"Section {name} is saved in database!")
        return {
            "message":f"{name} Added"
        }

@router.delete("/section")
def remove_section(
    name: str,
    manager: StorageManager = Depends(get_storage_manager)
    ):
        if name not in manager:
            LOGGER.error("%s not in the database", helper.get_name_parts(name, -1))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{helper.get_name_parts(name, -1)} not in the database"
                )
        
        del manager[name]
        manager.save()
        log_debug_and_info(LOGGER, f"Section {name} deleted from database!")

@router.post("/expense")
def add_expense_in_section(
    name: str,
    expense: float,
    manager: StorageManager = Depends(get_storage_manager)
    ):
        LOGGER.info("Adding expense in section %s", name)
        if name not in manager:
            LOGGER.error("%s not in the database", helper.get_name_parts(name, -1))
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{helper.get_name_parts(name, -1)} not in the database"
                )

        if manager[name]['limit'] < expense:
            LOGGER.error("%s is not permitted to go beyond limit of %s", helper.get_name_parts(name, -1), manager[name]['limit'])
            raise HTTPException(
                status_code=status.HTTP_417_EXPECTATION_FAILED,
                detail=f"{helper.get_name_parts(name, -1)} is not permitted to go beyond limit of {manager[name]['limit']}"
                )
        manager[name]['expense'] = expense
        manager.save()
        LOGGER.info("Expense added in section %s", name)
        
        return {"message": f"Expense added in section {helper.get_name_parts(name, -1)}", "expense": expense}


@router.put("/expense")
def update_expense_in_section(
    name: str,
    additional_expense: float,
    manager: StorageManager = Depends(get_storage_manager)
):
    LOGGER.info("Updating expense in section %s", name)

    if name not in manager:
        LOGGER.error("%s not in the database", helper.get_name_parts(name, -1))
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{helper.get_name_parts(name, -1)} not in the database"
        )

    current_expense = manager[name]['expense']
    limit = manager[name]['limit']
    new_expense = current_expense + additional_expense

    if new_expense > limit:
        LOGGER.error(
            "%s cannot exceed limit %s (current: %s, attempted: %s)",
            helper.get_name_parts(name, -1), limit, current_expense, additional_expense
        )
        raise HTTPException(
            status_code=status.HTTP_417_EXPECTATION_FAILED,
            detail=f"{helper.get_name_parts(name, -1)} cannot exceed limit {limit} (current: {current_expense}, attempted: {additional_expense})"
        )

    manager[name]['expense'] = new_expense
    manager.save()
    LOGGER.info("Expense updated in section %s, new total: %s", name, new_expense)

    return {"message": f"Expense updated in section {name}", "new_total": new_expense}
