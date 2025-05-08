from fastapi import APIRouter, HTTPException, Depends, status
from utils.StorageManager import  StorageManager, get_storage_manager
from utils import helper

router = APIRouter(prefix="/add", tags=["Section"])


@router.post("/section")
def add_section_in_storage(
    name: str,
    limit:float,
    manager: StorageManager = Depends(get_storage_manager)
    ):
        if name in manager:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{helper.get_name_parts(name,-1)} already in {helper.get_name_parts(name,-2)}"
            )
        
        maximum_expense_limit = manager.get_propagated_limit_for_child(name)
        if not (manager.get_immidiate_parent_limit(name) >= limit and maximum_expense_limit >= limit):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"{helper.get_name_parts(name,-1)} is having more expense than {helper.get_name_parts(name,-2)} cannot add!"
            )
        manager[name] = {
            "limit": limit,
            "expense":0
        }

        manager.save()

        return {
            "message":f"{name} Added"
        }