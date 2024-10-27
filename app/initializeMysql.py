from contextlib import contextmanager
import pymysql
from . import config

# Used for the first time when the database is not created yet.
# For other circumstances, use get_connection() from mysql_funcs.py
@contextmanager
def get_connection():
    try:
        if config.mode == "PRD":
            #-------------------Production environment-------------------#
            connection = pymysql.connect(host=config.mysql_PRD["host"],
                                        user=config.mysql_PRD["user"],
                                        password=config.mysql_PRD["password"],
                                        port=config.mysql_PRD["port"],
                                        cursorclass=pymysql.cursors.DictCursor,)
        elif config.mode == "QAS":
            #-------------------QAS environment-------------------#
            connection = pymysql.connect(host=config.mysql_QAS["host"],
                                        user=config.mysql_QAS["user"],
                                        password=config.mysql_QAS["password"],
                                        port=config.mysql_QAS["port"],
                                        cursorclass=pymysql.cursors.DictCursor,)
        elif config.mode == "DEV":
            #-------------------Developer environment-------------------#
            connection = pymysql.connect(host=config.mysql_DEV["host"],
                                        user=config.mysql_DEV["user"],
                                        password=config.mysql_DEV["password"],
                                        port=config.mysql_DEV["port"],
                                        cursorclass=pymysql.cursors.DictCursor,)
    except:
        raise Exception("Failed to connect to MySQL")
    try:
        yield connection
    finally:
        connection.close()


with get_connection() as db:
    cursor = db.cursor()
    # Check if database exists
    if not cursor.execute(f"SHOW DATABASES like '{config.mysql['database']}'"):
        # Create a database if it doesn't not exist 
        print(f"create {config.mysql['database']} database")
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + config.mysql["database"])
        print(f"create {config.mysql['database']} done")
    else:
        print(f"{config.mysql['database']} database exists.")

    # Select database
    print(f"select {config.mysql['database']} database")
    db.select_db(config.mysql["database"])

    # Create table-1
    table = config.mysql["table-1"]
    print(f"Set up table: {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"Table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0] == 1146:
            print(f"e.args: {e.args}")
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ID VARCHAR(10),
                    PRIMARY KEY (ID),
                    COL1 VARCHAR(250),
                    COL2 VARCHAR(20),
                    COL3 INT,
                    COL4 FLOAT,
                    MYDATE DATE,
                    )"""
            cursor.execute(sql)
            print(f"Table {table} created successfully.")
        else :
            print(f"Table {table} created unsuccessfully.")

    # Create table-2
    table = config.mysql["table-2"]
    print(f"Set up table: {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"Table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0] == 1146:
            print(f"e.args: {e.args}")
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ID VARCHAR(10),
                    PRIMARY KEY (ID),
                    COL1 VARCHAR(50),
                    COL2 FLOAT,
                    COL3 INT,
                    COL4 INT,
                    MYDATE DATE,
                    )"""
            cursor.execute(sql)
            print(f"Table {table} created successfully.")
        else :
            print(f"Table {table} created unsuccessfully.")