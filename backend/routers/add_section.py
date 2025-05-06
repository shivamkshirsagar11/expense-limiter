from fastapi import APIRouter, HTTPException, Depends, status
from utils.StorageManager import  StorageManager, get_storage_manager

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
                detail=f"{name} already in db"
            )
        manager[name] = {
            "limit": limit
        }
        manager.save()

        return {
            "message":f"{name} Added"
        }