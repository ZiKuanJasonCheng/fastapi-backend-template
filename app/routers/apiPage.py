from .. import logger, config
from app.database.mysql_funcs import get_data, insert_update_data
from typing import List
from fastapi import Query, APIRouter
from pydantic import BaseModel

myLogger = logger.get_logger("apiPage", "apiPage.log")
router = APIRouter()

@router.on_event("startup")
async def startup_event():
    """
        Startup event handler
    """
    return {"msg": "Startup event handler"}

@router.on_event("shutdown")
async def shutdown_event():
    """
        Shutdown event handler
    """
    return {"msg": "Shutdown event handler"}

@router.get("/getAllData", tags=["apiPage"], description="Get all data from DB")
async def getAllData():
    result = get_data(mysql_cmd=f"SELECT * FROM {config.mysql['table-1']}", logger=myLogger)
    return result


class ParamSet1(BaseModel):
    param1: str = Query(None, description="param1")
    param2: int = Query(None, description="param2")
    param3: List[str] = Query(None, description="param3")

@router.post("/updateData", tags=["apiPage"], description="Update data")
async def updateData(item: ParamSet1):
    if item.param1 == "yyy":
        raise("param1 cannot be yyy!")
    if item.param2 == -1:
        raise("param2 cannot be -1!")
    if len(item.param3) == 0:
        raise("param3 cannot be an empty list!")

    status = insert_update_data(f"UPDATE {config.mysql['table-2']} SET COL1='{item.param1}' WHERE COL2={item.param2}")
    if status:
        return {"msg": "Successful"}
    else:
        return {"msg": "Failed"}
