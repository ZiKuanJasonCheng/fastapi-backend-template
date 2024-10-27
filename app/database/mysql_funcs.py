from contextlib import contextmanager
from logging import Logger
import pymysql
from sqlalchemy import create_engine
from urllib.parse import quote
from .. import config


@contextmanager
def get_connection():
    '''
        Create MySQL connection object using pymysql
        Return:
            A connection object
    '''
    try:
        if config.mode == "PRD":
            #-------------------Production environment-------------------#
            connection = pymysql.connect(host=config.mysql_PRD["host"],
                                        user=config.mysql_PRD["user"],
                                        password=config.mysql_PRD["password"],
                                        port=config.mysql_PRD["port"],
                                        database=config.mysql["database"],
                                        cursorclass=pymysql.cursors.DictCursor,)
        elif config.mode == "QAS":
            #-------------------QAS environment-------------------#
            connection = pymysql.connect(host=config.mysql_QAS["host"],
                                        user=config.mysql_QAS["user"],
                                        password=config.mysql_QAS["password"],
                                        port=config.mysql_QAS["port"],
                                        database=config.mysql["database"],
                                        cursorclass=pymysql.cursors.DictCursor,)
        else:   #config.mode == "DEV":
            #-------------------Developer environment-------------------#
            connection = pymysql.connect(host=config.mysql_DEV["externalDEV"],
                                        user=config.mysql_DEV["user"],
                                        password=config.mysql_DEV["password"],
                                        port=config.mysql_DEV["port"],
                                        database=config.mysql["database"],
                                        cursorclass=pymysql.cursors.DictCursor,)
    except:
        raise Exception("Failed to connect to MySQL database")
    try:
        yield connection
    finally:
        connection.close()

# SQLAlchemy way of MySQL connection settings
def get_mysql_settings():
    '''
        Create MySQL engine object using sqlalchemy
        Return:
            A SQLAlchemy engine object
    '''
    if config.mode == "PRD":
        url = f'mysql+pymysql://{config.mysql_PRD["user"]}:{config.mysql_PRD["password"]}@{config.mysql_PRD["host"]}:{config.mysql_PRD["port"]}/{config.mysql_PRD["database"]}'
    elif config.mode == "QAS":
        url = f'mysql+pymysql://{config.mysql_QAS["user"]}:{config.mysql_QAS["password"]}@{config.mysql_QAS["host"]}:{config.mysql_QAS["port"]}/{config.mysql_QAS["database"]}'
    else:  #config.mode == "DEV":
        url = f'mysql+pymysql://{config.mysql_DEV["user"]}:{config.mysql_DEV["password"]}@{config.mysql_DEV["host"]}:{config.mysql_DEV["port"]}/{config.mysql_DEV["database"]}'
    
    engine = create_engine(url)
    return engine

def get_data(
        mysql_cmd: str,
        logger: Logger
    ):
    '''
        Fetch data from MySQL table via MySQL command
        Inputs:
            mysql_cmd: MySQL command
            logger: Used for logging
        Return:
            data - If data are successfully fetched from database
            False - Otherwise
    '''
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(mysql_cmd)
            data = cursor.fetchall()
            cursor.close()
        return data
    except:
        logger.exception(f"Failed to fetch data from MySQL database")
        return False

def insert_update_data(
        list_data: list,
        mysql_cmd: str,
        logger: Logger
    ):
    '''
        Insert/Update data into MySQL table
        Inputs:
            list_data: A list of dictionaries containing data to be inserted or updated
            mysql_cmd: MySQL command
            logger: Used for logging
        Return:
            True - If data are successfully inserted/updated to database
            False - Otherwise
    '''
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Execute MySQL command to insert/update new data
            cursor.executemany(mysql_cmd, list_data)
            conn.commit()
            cursor.close()
            return True
    except:
        logger.exception(f"Failed to insert/update data to MySQL database")
        return False
        
def insert_update_data_in_batch(
        list_data: list,
        mysql_cmd: str,
        batch_size: int,
        logger: Logger
    ):
    '''
        Insert/Update data into MySQL table in batch. Use this function if there are gigantic numbers of data.
        Inputs:
            list_data: A list of dictionaries containing data to be inserted or updated
            mysql_cmd: MySQL command
            batch_size: How many data to insert or update for a batch
            logger: Used for logging
        Return:
            True - If data are successfully inserted/updated to database
            False - Otherwise
    '''
    batch_i = 0
    list_failed_batch = []
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            while batch_i*batch_size < len(list_data):
                list_batch = list_data[batch_i*batch_size: (batch_i+1)*batch_size]
                try:
                    logger.info(f"batch_i: {batch_i}. Ready to insert/update {len(list_batch)} batch data")
                    # Execute MySQL command to insert/update new data
                    cursor.executemany(mysql_cmd, list_data)
                    conn.commit()
                except:
                    logger.exception(f"Failed to insert/update {len(list_batch)} data. batch_i: {batch_i}")
                    logger.info(f"Failed top 10 batch data: {list_batch[:10]}")
                    list_failed_batch.append(batch_i)
                batch_i += 1

            cursor.close()
            logger.info(f"len(list_failed_batch): {len(list_failed_batch)}")
            logger.info(f"list_failed_batch: {list_failed_batch}")
            return True if len(list_failed_batch) == 0 else False
    except:
        logger.exception(f"Failed to connect to MySQL database")
        return False

def revise_data_with_sql(
        mysql_cmd: str, 
        logger: Logger
    ):
    '''
        Revise data in MySQL table. The operation can be deletion, update, etc.
        Inputs:
            mysql_cmd: MySQL command
            logger: Used for logging
        Return:
            True - If MySQL command is successfully executed
            False - Otherwise
    '''
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Execute MySQL command
            cursor.execute(mysql_cmd)
            conn.commit()
            cursor.close()
            return True
    except:
        logger.exception(f"Failed to execute MySQL command")
        return False
