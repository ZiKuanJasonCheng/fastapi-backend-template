import cx_Oracle
from logging import Logger
from sqlalchemy import create_engine

# SQLAlchemy way of Oracle connection settings
def get_oracle_settings(username, pwd, host, port, db):
    '''
        Create Oracle SQL engine object using sqlalchemy
        Return:
            A SQLAlchemy engine object
    '''
    url = f'oracle+cx_oracle://{username}:{pwd}@{host}:{port}/{db}'
    return create_engine(url)


def get_data(
        engine: cx_Oracle.Connection,
        cmd: str,
        logger: Logger
    ):
    '''
        Fetch data from Oracle SQL table via Oracle SQL command
        Inputs:
            engine: Oracle SQL engine for DB operation
            cmd: Oracle SQL command
            logger: Used for logging
        Return:
            list_results - If data are successfully fetched from database
            False - Otherwise
    '''
    try:
        with engine as conn:
            cursor = conn.conncursor()
            cursor.execute(cmd)
            list_colNames = []
            
            # Fetch column names
            for ele in cursor.description:
                list_colNames.append(ele[0])
            # Check if there are duplicate column names from different tables
            for colName in list_colNames:
                if list_colNames.count(colName) > 0:
                    index = 0
                    count = 0
                    while count < list_colNames.count(colName):
                        try:
                            # Search for item in list from index to the end of list
                            index = list_colNames.index(colName, index)
                            if count > 0:
                                list_colNames[index] += '_' + str(count)
                            index += 1
                            count += 1
                        except ValueError as e:
                            break
            #print("list_colNames=", list_colNames)
            data = cursor.fetchall()
            list_results = []
            for row in data:
                obj = {}
                for i, colName in enumerate(list_colNames):
                    obj[colName] = row[i]
                list_results.append(obj)
            cursor.close()
        return list_results
    except:
        logger.exception(f"Failed to fetch data from Oracle SQL database")
        return False