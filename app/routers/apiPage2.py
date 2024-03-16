from .. import logger, config
from pydantic.main import BaseModel
from typing import List
from fastapi.param_functions import Query
from fastapi.routing import APIRouter

myLogger = logger.get_logger("apiPage2", "apiPage2.log")
router = APIRouter()
    
@router.get('/getData', description="Get data from DB by parameters")
async def getDataByParams(
    param1: List[int]=Query(None, description="Parameter 1"),
    param2: float=Query(None, description="Parameter 2"),
    param3: str=Query(None, description="Parameter 3"),
):
    result = ...
    return result
