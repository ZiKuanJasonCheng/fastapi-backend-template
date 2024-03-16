# Import required packages
from logging import Logger
import datetime
import pandas as pd
import numpy as np
import cx_Oracle
import time
from sqlalchemy import create_engine
from ... import config
from ...database.mysql_funcs import (
    insert_update_data,
    insert_update_data_in_batch
)
from ...database.oracle_funcs import (
    getDataFromOracleDB,
)

async def task1(logger: Logger, date=None):
    '''
        Task 1: Fetch data from multiple databases (e.g. Oracle, PostgreSQL, ...), process data, and insert them 
        into MySQL table for front-end team to access
    '''
    
    try:
        logger.info(f"Connect to Oracle ORACLE_TABLE_NAME_1")
        db_oracle = cx_Oracle.connect(config.oracle["user-1"], config.oracle["password-1"], config.oracle["host-1"], encoding='UTF-8')
        list_data = getDataFromOracleDB(oracle=db_oracle, sql=f"SELECT * FROM ORACLE_TABLE_NAME_1 WHERE XX=YY")
        logger.info(f"list_data: {list_data}")
    except:
        logger.exception(f"Failed to retrieve data from Oracle ORACLE_TABLE_NAME_1")

    try:
        logger.info(f"Connect to PostgreSQL POSTGRESQL_TABLE_2")
        url = f'postgresql://{config.postgresql["user-2"]}:{config.postgresql["password-2"]}@{config.postgresql["host-2"]}:{config.postgresql["port-2"]}/{config.postgresql["database-2"]}'
        engine = create_engine(url)
        df_data = pd.read_sql_query(f"SELECT * FROM POSTGRESQL_TABLE_2 WHERE XX=YY", con=engine)
        logger.info(f"df_data: {df_data}")
    except:
        logger.exception(f"Failed to retrieve data from PostgreSQL POSTGRESQL_TABLE_2")

    # Do some data processing tasks here
    # ...
    list_processed_data = [...]
    
    # Insert processed data into our MySQL table
    status = insert_update_data_in_batch(list_data=list_processed_data, mysql_cmd=config.mysql_cmds["insert_table-1"], batch_size=2000, logger=logger)
    if not status:
        raise (f"Failed to insert data to MySQL {config.mysql['table-1']}")
    
    logger.info(f"Done!")

if __name__ == "__main__":
    import asyncio
    from app import logger
    logger = logger.get_logger("task1", "task1.txt")
    # Run the function directly for test
    asyncio.run(task1(logger))
