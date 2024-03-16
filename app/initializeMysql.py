from contextlib import contextmanager
import pymysql
from . import config
#from database.mysql_funcs import get_connection

# Used for the first time when the database is not created yet.
# For other circumstances, use get_connection() from mysql_funcs.py
@contextmanager
def get_connection():
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
        connection = pymysql.connect(host=config.mysql_DEV["externalDEV"],
                                    user=config.mysql_DEV["user"],
                                    password=config.mysql_DEV["password"],
                                    port=config.mysql_DEV["port"],
                                    cursorclass=pymysql.cursors.DictCursor,)
    try:
        yield connection
    finally:
        connection.close()


with get_connection() as db:
    cursor = db.cursor()
    # Check of database exists
    if not cursor.execute(f"SHOW DATABASES like '{config.mysql['database']}'"):
        # create "assetsx" database if database doesn't not exist 
        print(f"create {config.mysql['database']} database")
        cursor.execute("CREATE DATABASE IF NOT EXISTS " + config.mysql["database"])
        print(f"create {config.mysql['database']} done")
    else:
        print(f"{config.mysql['database']} database exists.")

    # select "assetsx" database
    print(f"select {config.mysql['database']} database")
    db.select_db(config.mysql["database"])

    ## create tables for mapping ASSET_TRANSFER_RECORD name
    table = config.mysql["table-asset_transfer_record"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    MSGID  VARCHAR(20),
                    ASID VARCHAR(30),
                    PRIMARY KEY (MSGID, ASID),
                    NAME VARCHAR(250),
                    OUT_DEPT VARCHAR(20),
                    OUT_KEEP_ID VARCHAR(20),
                    OUT_KEEP_NAME VARCHAR(50),
                    IN_DEPT VARCHAR(20),
                    IN_KEEP_ID VARCHAR(20),
                    IN_KEEP_NAME VARCHAR(50),
                    CDATE DATE,
                    REASON VARCHAR(500),
                    UDATE DATE
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for mapping ASSET_REPAIR_RECORD name
    table = config.mysql["table-asset_repair_record"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    id BIGINT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (id),
                    PLANT  VARCHAR(10),
                    EPGROUP VARCHAR(30),
                    EPNAME VARCHAR(30),
                    ASID VARCHAR(30),
                    EXECUTOR VARCHAR(10),
                    CNAME VARCHAR(50),
                    START_TIME DATE,
                    END_TIME DATE,
                    WORK_TIME FLOAT,
                    ERROR_CODE VARCHAR(30),
                    NGREMARK VARCHAR(400),
                    NGCODE VARCHAR(2000),
                    REPAIR_CONTENT VARCHAR(2000),
                    UDATE DATE
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for Mariadb_Pcba_Mapping
    table = config.mysql["table-maptable_pcba"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    UDATE DATE,
                    ASSETS_NO VARCHAR(50),
                    site VARCHAR(50),
                    plant VARCHAR(50),
                    PRIMARY KEY (UDATE, ASSETS_NO, plant),
                    line VARCHAR(50),
                    equip_name VARCHAR(200)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")
    
    ## create tables for Pcba_Color
    table = config.mysql["table-pcba_color"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    Date DATE,
                    ASSETS_NO VARCHAR(50),
                    PRIMARY KEY (Date, ASSETS_NO),
                    plant VARCHAR(50),
                    line VARCHAR(50),
                    equip_name VARCHAR(200),
                    Red FLOAT,
                    Yellow FLOAT,
                    Green FLOAT,
                    Gray FLOAT, 
                    Disconnect FLOAT
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for OEE_Month
    # table = config.mysql["table-pcba_colorM"]
    # print(f"set up table : {table}")
    # try:
    #     cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
    #     print(f"table {table} exists.")
    # except pymysql.err.ProgrammingError as e:
    #     if e.args[0]==1146:
    #         print(e.args)
    #         # sql for create table
    #         sql = f"""CREATE TABLE {table} (
    #                 Month VARCHAR(50),
    #                 ASSETS_NO VARCHAR(50),
    #                 PRIMARY KEY (Month, ASSETS_NO),
    #                 plant VARCHAR(50),
    #                 line VARCHAR(50),
    #                 equip_name VARCHAR(200), 
    #                 OeeHalf FLOAT
    #                 )"""
    #         cursor.execute(sql)
    #         print(f"table: {table} created successfully.")
    #     else :
    #         print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAINTAINER_CHECKLIST
    table = config.mysql["table-asset_maintainer"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    id BIGINT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (id),
                    PUBLISHER_DEPT VARCHAR(50),
                    PUBLISHER_NAME VARCHAR(50),
                    PUBLISHER_EMPLID VARCHAR(50)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAINTAINED
    table = config.mysql["table-asset_maintained"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    id BIGINT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (id),
                    PUBLISHER_NAME VARCHAR(50),
                    PUBLISHER_EMPLID VARCHAR(50),
                    PUBLISHER_DEPT VARCHAR(50),
                    ASSETS_NO VARCHAR(50),
                    ASID VARCHAR(50),
                    STATUS VARCHAR(50),
                    STATUS_TIME DATETIME,
                    PUBLISHER_TIME DATETIME,
                    PUBLISHER_DESC VARCHAR(1000),
                    INDEX (ASSETS_NO),
                    INDEX (PUBLISHER_TIME),
                    INDEX (PUBLISHER_TIME, ASSETS_NO),
                    INDEX (ASID, PUBLISHER_TIME)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## update tables for ASSET_MAINTAINED
    table = config.mysql["table-asset_maintained"]
    print(f"set up table : {table}")
    try:
        querySql = f"""select count(*) as count from information_schema.columns where table_name = '{table}' and column_name = 'IDLE_REASON' """;
        cursor.execute(querySql)
        result = cursor.fetchall()
        count = 0
        if(len(result) > 0):
            count = result[0]["count"]
        if count == 0:
            sql = f"""ALTER TABLE {table} 
                    ADD COLUMN `IDLE_REASON` VARCHAR(1000) NULL DEFAULT NULL AFTER `PUBLISHER_DESC`,
                    ADD COLUMN `DEAL_METHOD` VARCHAR(1000) NULL DEFAULT NULL AFTER `IDLE_REASON`;"""
            cursor.execute(sql)
            print(f"table: {table} updated successfully.")
        print(f"table: {table} already has these columns")
    except Exception as e:
        print(f"table: {table} updated unsuccessfully.")

    ## create tables for ASSET_SITE_MAPPING
    table = config.mysql["table-asset_site_map"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    id BIGINT NOT NULL,
                    COST_DEPT VARCHAR(20),
                    SITE VARCHAR(20),
                    COST_DEPT_ORG VARCHAR(20),
                    COMPANY VARCHAR(20) DEFAULT '',
                    PRIMARY KEY (COST_DEPT, COMPANY),
                    UDATE DATE
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for OPM_REVENUE
    table = config.mysql["table-asset_opm"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    id BIGINT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (id),
                    plant VARCHAR(20),
                    period VARCHAR(20),
                    revenue decimal(10,0),
                    plantname VARCHAR(20)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAJOR
    table = config.mysql["table-asset_majortable"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(20),
                    PRIMARY KEY (ASSETS_NO),
                    ASID VARCHAR(30),
                    COMPANY VARCHAR(10),
                    BRAND VARCHAR(50),
                    CNAME VARCHAR(250),
                    MODEL VARCHAR(250),
                    SN VARCHAR(50),
                    COST_DEPT VARCHAR(20),
                    KEEP_DEPT VARCHAR(20),
                    USE_AREA VARCHAR(20),
                    EMPLID VARCHAR(20),
                    NAME VARCHAR(50),
                    LOCATION VARCHAR(250),
                    ITEM VARCHAR(20),
                    BCAT VARCHAR(100),
                    MCAT VARCHAR(50),
                    SCAT VARCHAR(50),
                    PRNO VARCHAR(30),
                    PONO VARCHAR(30),
                    DCNO VARCHAR(20),
                    CNNO VARCHAR(20),
                    DCTP VARCHAR(20),
                    BDTYPE VARCHAR(20),
                    CRTDATE DATE,
                    PRICE DECIMAL(15,5), 
                    NET_WORTH DECIMAL(15,5),
                    ORD_DATE DATE,
                    CUT_DATE DATE,
                    DEPRECIATION_YEAR VARCHAR(20),
                    MONTHLY_DEPRECIATION DECIMAL(12,2),
                    BUY_TYPE VARCHAR(10),
                    UDATE DATE,
                    CATEGORY VARCHAR(50),
                    CATEGORY_ENG VARCHAR(250),
                    STATUS VARCHAR(50),
                    PANO VARCHAR(30),
                    RTNO VARCHAR(20),
                    IMPN VARCHAR(20),
                    WARRANTY INT(11),
                    ENGINEER VARCHAR(20),
                    INDEX (ASSETS_NO, COMPANY, STATUS),
                    INDEX (ITEM, IMPN)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAJOR_HISTORY
    table = config.mysql["table-asset_majortable_history"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO  VARCHAR(20),
                    ASID VARCHAR(30),
                    COMPANY VARCHAR(10),
                    BRAND VARCHAR(50),
                    CNAME VARCHAR(250),
                    MODEL VARCHAR(250),
                    SN VARCHAR(50),
                    COST_DEPT VARCHAR(20),
                    KEEP_DEPT VARCHAR(20),
                    USE_AREA VARCHAR(20),
                    EMPLID VARCHAR(20),
                    NAME VARCHAR(50),
                    LOCATION VARCHAR(250),
                    ITEM VARCHAR(20),
                    BCAT VARCHAR(100),
                    MCAT VARCHAR(50),
                    SCAT VARCHAR(50),
                    PRNO VARCHAR(30),
                    PONO VARCHAR(30),
                    DCNO VARCHAR(20),
                    CNNO VARCHAR(20),
                    DCTP VARCHAR(20),
                    BDTYPE VARCHAR(50),
                    CRTDATE DATE,
                    PRICE DECIMAL(15,5), 
                    NET_WORTH DECIMAL(15,5),
                    ORD_DATE DATE,
                    CUT_DATE DATE,
                    DEPRECIATION_YEAR VARCHAR(20),
                    MONTHLY_DEPRECIATION DECIMAL(12,2),
                    BUY_TYPE VARCHAR(10),
                    UDATE DATE,
                    PRIMARY KEY (ASSETS_NO,UDATE),
                    CATEGORY VARCHAR(50),
                    CATEGORY_ENG VARCHAR(250),
                    STATUS VARCHAR(50),
                    PANO VARCHAR(30),
                    RTNO VARCHAR(20),
                    IMPN VARCHAR(20),
                    WARRANTY INT(11),
                    ENGINEER VARCHAR(20)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAJOR_HISTORY_DAILY
    table = config.mysql["table-asset_majortable_history_daily"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO  VARCHAR(20),
                    COMPANY VARCHAR(10),
                    STATUS VARCHAR(50),
                    UDATE DATE,
                    PRIMARY KEY (ASSETS_NO)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_CATEGORY
    table = config.mysql["table-asset_category"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    id BIGINT NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (id),
                    CNAME  VARCHAR(250),
                    CATEGORY VARCHAR(250)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_AREA
    table = config.mysql["table-asset_area"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    KEEP_DEPT VARCHAR(20),
                    PRIMARY KEY (KEEP_DEPT),
                    AREA VARCHAR(20)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")
    
    ## create tables for ASSET_POPR
    table = config.mysql["table-asset_popr"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(20),
                    PRIMARY KEY (ASSETS_NO),
                    PRNO VARCHAR(20),
                    PONO VARCHAR(20),
                    Eform_PN VARCHAR(50),
                    ITEM VARCHAR(20),
                    BCAT VARCHAR(50),
                    MCAT VARCHAR(50),
                    SCAT VARCHAR(50),
                    PANO VARCHAR(30)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAIL_RECORD
    table = config.mysql["table-asset_mailrecord"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ID BIGINT(20) NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (ID),
                    ASSETS_NO VARCHAR(50) NULL DEFAULT NULL,
                    DEPT_MGR_ID VARCHAR(50) NULL DEFAULT NULL,
                    DEPT_MGR_NAME VARCHAR(50) NULL DEFAULT NULL,
                    DEPT_MGR_MAIL VARCHAR(100) NULL DEFAULT NULL,
                    DIV_MGR_ID VARCHAR(50) NULL DEFAULT NULL,
                    DIV_MGR_NAME VARCHAR(50) NULL DEFAULT NULL,
                    DIV_MGR_MAIL VARCHAR(100) NULL DEFAULT NULL,
                    TIMERANGE VARCHAR(50) NULL DEFAULT NULL,
                    SEND_LEVEL INT(5) NOT NULL DEFAULT 0,
                    FIRST_SEND_DATE VARCHAR(50) NULL DEFAULT NULL,
                    SEND_DATE VARCHAR(50) NULL DEFAULT NULL,
                    SEND_TIMES INT(20) NOT NULL DEFAULT 1,
                    SIGN_DATE VARCHAR(50) NULL DEFAULT NULL,
                    SIGN_STATUS INT(5) NOT NULL DEFAULT 0
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MINOR
    table = config.mysql["table-asset_minor"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    MYFA_RNO VARCHAR(30),
                    ASSETS_NO VARCHAR(20),
                    ASID VARCHAR(20),
                    COMPANY VARCHAR(20),
                    PRIMARY KEY (MYFA_RNO, ASSETS_NO, COMPANY),
                    BRAND VARCHAR(50),
                    CNAME VARCHAR(100),
                    MODEL VARCHAR(80),
                    SN VARCHAR(50),
                    PRICE FLOAT(10, 2),
                    COST_DEPT VARCHAR(20),
                    SITE VARCHAR(20),
                    NET_WORTH FLOAT(10, 2),
                    MYFA_NRNO VARCHAR(20),
                    LAST_SIGNLOG_TIME DATE,
                    NEW_DEPT VARCHAR(10),
                    NEW_SITE VARCHAR(20),
                    SALE_PRICE FLOAT(10, 2),
                    SALE_CURRENCY VARCHAR(20),
                    NEW_BUYER VARCHAR(20),
                    NEW_BUYER_2 VARCHAR(80),
                    CATEGORY VARCHAR(1),
                    ROLLIN_BENEFIT FLOAT(10, 2),
                    ROLLOUT_BENEFIT FLOAT(10, 2),
                    TOTAL_BENEFIT FLOAT(10, 2),
                    STATUS VARCHAR(10),
                    UDATE DATE,
                    UTIME TIME
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_RENT
    table = config.mysql["table-asset_rent"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    PONO VARCHAR(20),
                    POLN VARCHAR(10),
                    PRIMARY KEY (PONO, POLN),
                    ASSETS_NO VARCHAR(20),
                    CNAME VARCHAR(100),
                    BRAND VARCHAR(20),
                    SITE VARCHAR(20),
                    QTY FLOAT,
                    UNIT VARCHAR(30),
                    MODEL VARCHAR(200),
                    SN VARCHAR(50),
                    CATEGORY VARCHAR(50),
                    BUY_PRICE FLOAT,
                    MONTHLY_DEPRECIATION FLOAT,
                    RENT_PRICE FLOAT,
                    RENT_CURRENCY VARCHAR(10),
                    RENT_START DATE,
                    RENT_END DATE,
                    RENT_DURATION_MONTHLY INT,
                    VENDOR VARCHAR(200),
                    BENEFIT FLOAT,
                    UDATE DATE
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_VENDOR
    table = config.mysql["table-asset_vendor"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    VENDOR_CODE VARCHAR(10),
                    PRIMARY KEY (VENDOR_CODE),
                    VENDOR VARCHAR(200)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAINTAINED_USERS
    table = config.mysql["table-asset_maintained_users"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        ASSET_MAINTAINED_USERS_ID BIGINT(20) NOT NULL AUTO_INCREMENT,
                        PRIMARY KEY (ASSET_MAINTAINED_USERS_ID),
                        EMP_NO VARCHAR(50) NULL DEFAULT NULL,
                        SITE VARCHAR(50) NULL DEFAULT NULL,
                        PLANT VARCHAR(50) NULL DEFAULT NULL,
                        EXTENT_OF_PURVIEW VARCHAR(50) NULL DEFAULT NULL,
                        ROLE VARCHAR(50) NULL DEFAULT NULL,
                        MAINTAIN_ID VARCHAR(50) NOT NULL,
                        MAINTAIN_NAME VARCHAR(100) NOT NULL,
                        UPDATE_TIME VARCHAR(50) NOT NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_CCA_INFOS
    table = config.mysql["table-asset_cca_infos"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        ASSET_CCA_INFOS_ID BIGINT(20) NOT NULL AUTO_INCREMENT,
                        PRIMARY KEY (ASSET_CCA_INFOS_ID),
                        CoCd VARCHAR(100) NULL DEFAULT NULL,
                        CostCtr VARCHAR(100) NULL DEFAULT NULL,
                        Name VARCHAR(100) NULL DEFAULT NULL,
                        ProfitCtr VARCHAR(100) NULL DEFAULT NULL,
                        FuncArea VARCHAR(100) NULL DEFAULT NULL,
                        ValidFrom VARCHAR(100) NULL DEFAULT NULL,
                        ValidTo VARCHAR(100) NULL DEFAULT NULL,
                        Plant VARCHAR(100) NULL DEFAULT NULL,	
                        MAINTAIN_ID VARCHAR(50) NOT NULL,
                        MAINTAIN_NAME VARCHAR(100) NOT NULL,
                        MAINTAIN_SITE VARCHAR(100) NOT NULL,
                        UPDATE_TIME VARCHAR(50) NOT NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_SECURITY_EQUIPS
    table = config.mysql["table-asset_security_equips"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        ASSET_SECURITY_EQUIPS_ID BIGINT(20) NOT NULL AUTO_INCREMENT,
                        PRIMARY KEY (ASSET_SECURITY_EQUIPS_ID),
                        ASSET_NO VARCHAR(100) NULL DEFAULT NULL,
                        ASID VARCHAR(100) NULL DEFAULT NULL,
                        SECURITY_REASON VARCHAR(100) NULL DEFAULT NULL,
                        MAINTAIN_ID VARCHAR(50) NOT NULL,
                        MAINTAIN_NAME VARCHAR(100) NOT NULL,
                        UPDATE_TIME VARCHAR(50) NOT NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAIL_RECORD_INEFFICIENT
    table = config.mysql["table-asset_mailrecord_inefficient"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ID BIGINT(20) NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (ID),
                    ASSETS_NO VARCHAR(50) NULL DEFAULT NULL,
                    IE_MGR_ID VARCHAR(50) NULL DEFAULT NULL,
                    IE_MGR_NAME VARCHAR(50) NULL DEFAULT NULL,
                    IE_MGR_MAIL VARCHAR(100) NULL DEFAULT NULL,
                    IE_SIGN_DATE VARCHAR(50) NULL DEFAULT NULL,
                    IE_SIGN_RESULT VARCHAR(50) NULL DEFAULT NULL,
                    IE_REJECT_REASON VARCHAR(100) NULL DEFAULT NULL,
                    DIV_MGR_ID VARCHAR(50) NULL DEFAULT NULL,
                    DIV_MGR_NAME VARCHAR(50) NULL DEFAULT NULL,
                    DIV_MGR_MAIL VARCHAR(100) NULL DEFAULT NULL,
                    DIV_SIGN_DATE VARCHAR(50) NULL DEFAULT NULL,
                    DIV_SIGN_RESULT VARCHAR(50) NULL DEFAULT NULL,
                    DIV_REJECT_REASON VARCHAR(100) NULL DEFAULT NULL,
                    TIMERANGE VARCHAR(50) NULL DEFAULT NULL,
                    SEND_LEVEL INT(5) NOT NULL DEFAULT 0,
                    FIRST_SEND_DATE VARCHAR(50) NULL DEFAULT NULL,
                    SEND_DATE VARCHAR(50) NULL DEFAULT NULL,
                    SEND_TIMES INT(20) NOT NULL DEFAULT 1,
                    SIGN_DATE VARCHAR(50) NULL DEFAULT NULL,
                    SIGN_STATUS INT(5) NOT NULL DEFAULT 0
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")
    
    ## create tables for ASSET_VISITOR_TIMES
    table = config.mysql["table-asset_visitor_times"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        Date DATE NOT NULL,
                        PRIMARY KEY (Date),                        
                        VISITORS BIGINT(20) 
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_UNABLE_CONNECT
    table = config.mysql["table-asset_unable_connect"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSET_UNABLE_CONNECT_ID BIGINT(20) NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (ASSET_UNABLE_CONNECT_ID),
                    ASSETS_NO VARCHAR(50) NOT NULL DEFAULT '',
                    REASON VARCHAR(500) NOT NULL DEFAULT '',
                    DESCRIPTION VARCHAR(1000) NULL DEFAULT '',
                    CONFIRM_USERID VARCHAR(50) NULL DEFAULT '',
                    CONFIRM_TIME DATE NULL DEFAULT NULL
                )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_DEPT_SITE
    table = config.mysql["table-asset_dept_site"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ID BIGINT(20) NOT NULL AUTO_INCREMENT,
                    PRIMARY KEY (ID),
                    DEPT VARCHAR(50) NOT NULL DEFAULT '',
                    SITE VARCHAR(50) NOT NULL DEFAULT ''
                )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")
    
    ## create tables for ASSET_MAINTAINED_SIGN
    table = config.mysql["table-asset_maintained_sign"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    `ASSET_MAINTAINED_SIGN_ID` BIGINT(20) NOT NULL AUTO_INCREMENT,
                    `MAINTAIN_SIGN_NO` VARCHAR(50) NULL DEFAULT NULL,
                    `ASSETS_NO` VARCHAR(50) NULL DEFAULT NULL,
                    `PUBLISHER_NAME` VARCHAR(50) NULL DEFAULT NULL,
                    `PUBLISHER_EMPLID` VARCHAR(100) NULL DEFAULT NULL,
                    `PUBLISHER_DEPT` VARCHAR(50) NULL DEFAULT NULL,
                    `PUBLISHER_TIME` DATETIME NULL DEFAULT NULL,
                    `PUBLISHER_DESC` VARCHAR(1000) NULL DEFAULT NULL,
                    `IDLE_REASON` VARCHAR(1000) NULL DEFAULT NULL,
                    `DEAL_METHOD` VARCHAR(1000) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_EQUIP_STATUS` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_SEND_DATE` DATETIME NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_SEND_USER_ID` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_SEND_USER_NAME` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_PROSEDURE` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_USER_ID` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_USER_NAME` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_STATUS` INT(5) NOT NULL DEFAULT 0,
                    `MAINTAIN_SIGN_DATE` DATETIME NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_REMARK` VARCHAR(1000) NULL DEFAULT NULL,
                    `ASSET_MAIL_IDLE_ID` VARCHAR(50) NULL DEFAULT NULL,
                    `ASSET_MAIL_INEFFICIENT_ID` VARCHAR(50) NULL DEFAULT NULL,
                    PRIMARY KEY (`ASSET_MAINTAINED_SIGN_ID`)
                )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_MAINTAINED_SIGN_MAIL_RECORD
    table = config.mysql["table-asset_maintained_sign_mail_record"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    `ID` BIGINT(20) NOT NULL AUTO_INCREMENT,
                    `MAINTAIN_SIGN_NO` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_USER_ID` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_SIGN_USER_NAME` VARCHAR(50) NULL DEFAULT NULL,
                    `FIRST_SEND_DATE` VARCHAR(50) NULL DEFAULT NULL,
                    `SEND_DATE` VARCHAR(50) NULL DEFAULT NULL,
                    `SEND_TIMES` INT(20) NOT NULL DEFAULT 1,
                    `SIGN_DATE` VARCHAR(50) NULL DEFAULT NULL,
                    `SIGN_STATUS` INT(5) NOT NULL DEFAULT 0,
                    PRIMARY KEY (`ID`)
                )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## update tables for ASSET_MAIL_RECORD_INEFFICIENT
    table = config.mysql["table-asset_mailrecord_inefficient"]
    print(f"set up table : {table}")
    try:
        querySql = f"""select count(*) as count from information_schema.columns where table_name = '{table}' and column_name = 'DEPT_MGR_ID' """;
        cursor.execute(querySql)
        result = cursor.fetchall()
        count = 0
        if(len(result) > 0):
            count = result[0]["count"]
        if count == 0:
            sql = f"""ALTER TABLE {table} 
                    ADD COLUMN `DEPT_MGR_ID` VARCHAR(50) NULL DEFAULT NULL AFTER `ASSETS_NO`,
                    ADD COLUMN `DEPT_MGR_NAME` VARCHAR(50) NULL DEFAULT NULL AFTER `DEPT_MGR_ID`,
                    ADD COLUMN `DEPT_MGR_MAIL` VARCHAR(100) NULL DEFAULT NULL AFTER `DEPT_MGR_NAME`,
                    ADD COLUMN `DEPT_SIGN_DATE` VARCHAR(50) NULL DEFAULT NULL AFTER `DEPT_MGR_MAIL`,
                    ADD COLUMN `DEPT_SIGN_RESULT` VARCHAR(50) NULL DEFAULT NULL AFTER `DEPT_SIGN_DATE`,
                    ADD COLUMN `DEPT_REJECT_REASON` VARCHAR(100) NULL DEFAULT NULL AFTER `DEPT_SIGN_RESULT`;"""
            cursor.execute(sql)
            print(f"table: {table} updated successfully.")
        print(f"table: {table} already has these columns")
    except Exception as e:
        print(f"table: {table} updated unsuccessfully.")

    ## create tables for ASSET_ONLINE_MAINTAIN
    table = config.mysql["table-asset_online_maintain"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    `ASSET_ONLINE_MAINTAIN_ID` BIGINT(20) NOT NULL AUTO_INCREMENT,
                    `SITE` VARCHAR(50) NULL DEFAULT NULL,
                    `START_DATE` DATE NULL DEFAULT NULL,
                    `END_DATE` DATE NULL DEFAULT NULL,
                    `MAINTAIN_USER` VARCHAR(50) NULL DEFAULT NULL,
                    `MAINTAIN_DATE` DATETIME NULL DEFAULT NULL,
                    `MAINTAIN_STATUS` VARCHAR(50) NULL DEFAULT NULL,
                    PRIMARY KEY (`ASSET_ONLINE_MAINTAIN_ID`)
                )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")
    
    ## create tables for ASSET_ONLINE_MAINTAIN_DETAILS
    table = config.mysql["table-asset_online_maintain_details"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    `ASSET_ONLINE_MAINTAIN_DETAILS_ID` BIGINT(20) NOT NULL AUTO_INCREMENT,
                    `ASSET_ONLINE_MAINTAIN_ID` VARCHAR(50) NULL DEFAULT NULL,
                    `ONLINE_DATE` DATE NULL DEFAULT NULL,
                    `PLANNED_ONLINE_COUNT` INT(20) NULL DEFAULT NULL,
                    PRIMARY KEY (`ASSET_ONLINE_MAINTAIN_DETAILS_ID`)
                )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_PN_MAINTAIN
    table = config.mysql["table-asset_pn_maintain"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(20),
                    ASID VARCHAR(30),
                    PRIMARY KEY (ASSETS_NO, ASID),
                    IMPN VARCHAR(20) NOT NULL,
                    UDATE DATE NOT NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_EMS
    table = config.mysql["table-asset_ems"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(20),
                    ASID VARCHAR(30),
                    PRIMARY KEY (ASID),
                    COMPANY VARCHAR(10),
                    BRAND VARCHAR(50),
                    CNAME VARCHAR(250),
                    MODEL VARCHAR(250),
                    SN VARCHAR(50),
                    COST_DEPT VARCHAR(20),
                    KEEP_DEPT VARCHAR(20),
                    USE_AREA VARCHAR(20),
                    EMPLID VARCHAR(20),
                    NAME VARCHAR(50),
                    LOCATION VARCHAR(250),
                    ITEM VARCHAR(20),
                    BCAT VARCHAR(100),
                    MCAT VARCHAR(50),
                    SCAT VARCHAR(50),
                    PRNO VARCHAR(30),
                    PONO VARCHAR(30),
                    DCNO VARCHAR(20),
                    CNNO VARCHAR(20),
                    DCTP VARCHAR(20),
                    BDTYPE VARCHAR(20),
                    CRTDATE DATE,
                    PRICE DECIMAL(15,5), 
                    NET_WORTH DECIMAL(15,5),
                    ORD_DATE VARCHAR(10),
                    CUT_DATE VARCHAR(10),
                    DEPRECIATION_YEAR VARCHAR(20),
                    MONTHLY_DEPRECIATION VARCHAR(15),
                    BUY_TYPE VARCHAR(10),
                    UDATE DATE,
                    CATEGORY VARCHAR(50),
                    CATEGORY_ENG VARCHAR(250),
                    STATUS VARCHAR(50),
                    PANO VARCHAR(30),
                    RTNO VARCHAR(20),
                    IMPN VARCHAR(20),
                    WARRANTY INT(11),
                    ENGINEER VARCHAR(20),
                    INDEX (ASID, COMPANY, STATUS)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_EMS_HISTORY
    table = config.mysql["table-asset_ems_history"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(20),
                    ASID VARCHAR(30),
                    COMPANY VARCHAR(10),
                    BRAND VARCHAR(50),
                    CNAME VARCHAR(250),
                    MODEL VARCHAR(250),
                    SN VARCHAR(50),
                    COST_DEPT VARCHAR(20),
                    KEEP_DEPT VARCHAR(20),
                    USE_AREA VARCHAR(20),
                    EMPLID VARCHAR(20),
                    NAME VARCHAR(50),
                    LOCATION VARCHAR(250),
                    ITEM VARCHAR(20),
                    BCAT VARCHAR(100),
                    MCAT VARCHAR(50),
                    SCAT VARCHAR(50),
                    PRNO VARCHAR(30),
                    PONO VARCHAR(30),
                    DCNO VARCHAR(20),
                    CNNO VARCHAR(20),
                    DCTP VARCHAR(20),
                    BDTYPE VARCHAR(20),
                    CRTDATE DATE,
                    PRICE DECIMAL(15,5), 
                    NET_WORTH DECIMAL(15,5),
                    ORD_DATE DATE,
                    CUT_DATE DATE,
                    DEPRECIATION_YEAR VARCHAR(20),
                    MONTHLY_DEPRECIATION DECIMAL(12,2),
                    BUY_TYPE VARCHAR(10),
                    UDATE DATE,
                    PRIMARY KEY (ASID, UDATE),
                    CATEGORY VARCHAR(50),
                    CATEGORY_ENG VARCHAR(250),
                    STATUS VARCHAR(50),
                    PANO VARCHAR(30),
                    RTNO VARCHAR(20),
                    IMPN VARCHAR(20),
                    WARRANTY INT(11),
                    ENGINEER VARCHAR(20),
                    INDEX (ASID, COMPANY, STATUS)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_ACPT
    table = config.mysql["table-asset_acpt"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    PLANTCODE VARCHAR(10),
                    BUYER VARCHAR(10),
                    BUYN VARCHAR(30),
                    PRNO VARCHAR(20),
                    PRLN VARCHAR(5),
                    SPEC VARCHAR(200),
                    PONO VARCHAR(20),
                    POLN VARCHAR(5),
                    PO_DATE VARCHAR(10),
                    PARTNO VARCHAR(70),
                    VEND VARCHAR(10),
                    VDESC VARCHAR(100),
                    RTNO VARCHAR(10) NOT NULL,
                    RTLN VARCHAR(5),
                    RTDATE DATE,
                    RQTY INT,
                    FINAL_PRICE DECIMAL(15,5),
                    FINAL_PRICE_RMB DECIMAL(15,5),
                    CURR VARCHAR(5),
                    ADAYS INT,
                    ADLDATE DATE,
                    PRAPPID VARCHAR(10),
                    PRAPPN VARCHAR(30),
                    PRAPPD VARCHAR(10),
                    ISACCEPTANCE VARCHAR(5),
                    ACPTNO VARCHAR(20),
                    ACPTDATE DATE,
                    ACPTUSER VARCHAR(10),
                    AQTY INT,
                    WAITINGUSER VARCHAR(10),
                    PENDINGDATE FLOAT,
                    ACPT_APPROVE_DATE DATE,
                    PANO VARCHAR(30),
                    APLDAT DATE,
                    APPROVDAT DATE,
                    STATUS VARCHAR(10),
                    TOTAL_PRICE DECIMAL(15,5),
                    TOTAL_PRICE_RMB DECIMAL(15,5),
                    NO_ACPT_DATE INT,
                    ACPT_PENDING_DATE INT,
                    TOTAL_AGING_DATE INT,
                    UDATE DATE NOT NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_PA
    table = config.mysql["table-asset_pa"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    PLANTCODE VARCHAR(10),
                    BUYER VARCHAR(10),
                    BUYN VARCHAR(30),
                    PRNO VARCHAR(20),
                    PRLN VARCHAR(5),
                    SPEC VARCHAR(200),
                    PONO VARCHAR(20),
                    POLN VARCHAR(5),
                    PO_DATE VARCHAR(10),
                    PARTNO VARCHAR(70),
                    VEND VARCHAR(10),
                    VDESC VARCHAR(100),
                    RTNO VARCHAR(10) NOT NULL,
                    RTLN VARCHAR(5),
                    RTDATE DATE,
                    RQTY INT,
                    FINAL_PRICE DECIMAL(15,2),
                    FINAL_PRICE_RMB DECIMAL(15,2),
                    CURR VARCHAR(5),
                    ADAYS INT,
                    ADLDATE DATE,
                    PRAPPID VARCHAR(10),
                    PRAPPN VARCHAR(30),
                    PRAPPD VARCHAR(10),
                    ISACCEPTANCE VARCHAR(5),
                    ACPTNO VARCHAR(20),
                    ACPTDATE DATE,
                    ACPTUSER VARCHAR(10),
                    AQTY INT,
                    WAITINGUSER VARCHAR(10),
                    PENDINGDATE FLOAT,
                    ACPT_APPROVE_DATE DATE,
                    PANO VARCHAR(30),
                    APLDAT DATE,
                    APPROVDAT DATE,
                    STATUS VARCHAR(10),
                    TOTAL_PRICE DECIMAL(15,2),
                    TOTAL_PRICE_RMB DECIMAL(15,2),
                    PENDING_DAYS INT,
                    RT_TO_ACPT_DAYS INT,
                    TOTAL_AGING_DAYS INT,
                    PA_TO_TODAY_DAYS INT,
                    FINAL_QTY INT,
                    UDATE DATE NOT NULL,
                    PEND_APPROVERID VARCHAR(20),
                    PEND_ENAME VARCHAR(30),
                    PEND_STARTDATE DATE,
                    PEND_TOTALDATE INT,
                    PA_STATUS INT,
                    SEND_TO_FIN_DATE DATE,
                    INDEX (PLANTCODE),
                    INDEX (STATUS),
                    INDEX (PENDING_DAYS)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ## create tables for ASSET_EXCH_RATE
    table = config.mysql["table-asset_exch_rate"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    CCURDATE DATE,
                    RATIOFROM INT(5),
                    CCURFROM VARCHAR(5),
                    RATIOTO INT(5),
                    CCURTO VARCHAR(5),
                    PRIMARY KEY (CCURDATE, RATIOFROM, CCURFROM, RATIOTO, CCURTO),
                    CCURRATE DECIMAL(15, 5),
                    UDATE DATE
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else :
            print(f"table: {table} created unsuccessfully.")

    ##create tables for ASSET_LOCK_STATUS
    table = config.mysql["table-asset_lock_status"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(50) NOT NULL,
                    ASID VARCHAR(50) NOT NULL,
                    MINOR_NO VARCHAR(50) NULL DEFAULT '',
                    MINOR_CATG VARCHAR(50) NULL DEFAULT '',
                    LOCK_TYPE VARCHAR(50) NULL DEFAULT '',
                    STATUS VARCHAR(50) NULL DEFAULT 'LOCK',
                    UDATE DATETIME NULL DEFAULT NULL,
                    PRIMARY KEY (ASSETS_NO, ASID)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")

    ##create tables for ASSET_NOT_CREDITED
    table = config.mysql["table-asset_not_credited"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    PA_NO VARCHAR(20),
                    PA_LINE VARCHAR(5),
                    CHARGE_DEPT VARCHAR(10),
                    CHARGE_SITE VARCHAR(10),
                    CHARGE_PERCENTAGE VARCHAR(10),
                    CHARGE_PERCENTAGE_2 DECIMAL(15, 5),
                    TOTAL_AMOUNT DECIMAL(15, 5),
                    TOTAL_TAX DECIMAL(15, 5),
                    TOTAL_ALL DECIMAL(15, 5),
                    TOTAL_AMOUNT_RMB DECIMAL(15, 5),
                    TOTAL_TAX_RMB DECIMAL(15, 5),
                    TOTAL_ALL_RMB DECIMAL(15, 5),
                    CHARGE_AMOUNT DECIMAL(15, 5),
                    CHARGE_TAX DECIMAL(15, 5),
                    CHARGE_TOTAL_ALL DECIMAL(15, 5),
                    CHARGE_AMOUNT_RMB DECIMAL(15, 5),
                    CHARGE_TAX_RMB DECIMAL(15, 5),
                    CHARGE_TOTAL_ALL_RMB DECIMAL(15, 5),
                    SITE_AMOUNT DECIMAL(15, 5),
                    SITE_TAX DECIMAL(15, 5),
                    SITE_TOTAL_ALL DECIMAL(15, 5),
                    SITE_AMOUNT_RMB DECIMAL(15, 5),
                    SITE_TAX_RMB DECIMAL(15, 5),
                    SITE_TOTAL_ALL_RMB DECIMAL(15, 5),
                    INVOICE_NO VARCHAR(20),
                    PO_NO VARCHAR(20),
                    PO_LINE VARCHAR(10),
                    RT_NO VARCHAR(20),
                    RT_LINE VARCHAR(20),
                    COMPANY_CODE VARCHAR(10),
                    COMPANY VARCHAR(10),
                    VENDOR_CODE VARCHAR(10),
                    VENDOR_NAME VARCHAR(100),
                    CURRENCY VARCHAR(5),
                    CREATEDBY VARCHAR(30),
                    PA_STATUS_CODE VARCHAR(5),
                    PA_STATUS_DECS VARCHAR(100),
                    SEND_FIN_DATE DATE,
                    FIN_ACPT_DATE DATE,
                    UNACPT_FINE_DAY INT(10),
                    ACPT_NO VARCHAR(20),
                    UDATE DATE
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")

    ##create tables for ASSET_TR_LIST
    table = config.mysql["table-asset_tr_list"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1146:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(20) NOT NULL,
                    ASID VARCHAR(20) NOT NULL,
                    TR_NO VARCHAR(20) NOT NULL,
                    ORG_DEPT VARCHAR(10) NOT NULL,
                    ORG_SITE VARCHAR(10) NOT NULL,
                    NEW_DEPT VARCHAR(10) NOT NULL,
                    NEW_SITE VARCHAR(10) NOT NULL,
                    TR_DATE DATETIME NOT NULL,
                    UDATE DATE NOT NULL,
                    `ORDER` INT NOT NULL DEFAULT 1,
                    LAST_TR_DATE DATETIME,
                    NEXT_TR_DATE DATETIME,
                    ONLINE_DATE DATETIME
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")

    ##create tables for ASSET_OEE_BYMONTH
    table = config.mysql["table-asset_oeem_bymonth"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    `Month` VARCHAR(50) NOT NULL,
                    ASSETS_NO VARCHAR(100) NOT NULL,
                    ASID VARCHAR(100) NOT NULL,
                    ONLINE_DATE VARCHAR(50) NULL DEFAULT NULL,
                    USE_TIME_HOUR FLOAT NULL DEFAULT NULL,
                    OEE FLOAT NULL DEFAULT NULL,
                    PRIMARY KEY (`Month`, `ASSETS_NO`, `ASID`)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")

    ## update tables for ASSET_MAIL_RECORD
    table = config.mysql["table-asset_mailrecord"]
    print(f"set up table : {table}")
    try:
        querySql = f"""select count(*) as count from information_schema.columns where table_name = '{table}' and column_name IN ('ENGINEER_DEPT_MGR_ID','ENGINEER_DEPT_MGR_NAME','ENGINEER_DEPT_MGR_MAIL')  """;       
        cursor.execute(querySql)
        result = cursor.fetchall()
        count = 0
        if(len(result) > 0):
            count = result[0]["count"]
        if count == 0:
            sql = f"""ALTER TABLE {table} 
                    ADD COLUMN ENGINEER_DEPT_MGR_MAIL VARCHAR(100) NULL DEFAULT NULL AFTER DIV_MGR_MAIL,
                    ADD COLUMN ENGINEER_DEPT_MGR_NAME VARCHAR(50) NULL DEFAULT NULL AFTER DIV_MGR_MAIL,
                    ADD COLUMN ENGINEER_DEPT_MGR_ID VARCHAR(50) NULL DEFAULT NULL AFTER DIV_MGR_MAIL ;"""
            cursor.execute(sql)
            print(f"table: {table} updated successfully.")
        print(f"table: {table} already has these columns")
    except Exception as e:
        print(f"table: {table} updated unsuccessfully.")

    ## update tables for ASSET_MAIL_RECORD_INEFFICIENT
    table = config.mysql["table-asset_mailrecord_inefficient"]
    print(f"set up table : {table}")
    try:
        querySql = f"""select count(*) as count from information_schema.columns where table_name = '{table}' and column_name = 'ASID' """;
        cursor.execute(querySql)
        result = cursor.fetchall()
        count = 0
        if(len(result) > 0):
            count = result[0]["count"]
        if count == 0:
            sql = f"""ALTER TABLE {table} 
                    ADD COLUMN `ASID` VARCHAR(50) NULL DEFAULT NULL AFTER `ASSETS_NO`;"""
            cursor.execute(sql)
            print(f"table: {table} updated successfully.")
        print(f"table: {table} already has these columns")
    except Exception as e:
        print(f"table: {table} updated unsuccessfully.")

    ##create tables for ASSET_ONLINE_PIC
    table = config.mysql["table-asset_online_pic"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                    ASSETS_NO VARCHAR(50) NOT NULL,
                    ASID VARCHAR(50) NOT NULL,
                    ONLINE_DATE VARCHAR(50) NULL DEFAULT NULL,
                    ONLINE_PIC_CNAME VARCHAR(50) NULL DEFAULT NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")
            
    ##create tables for ASSET_ACPT_REASON
    table = config.mysql["table-asset_acpt_reason"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        `PONO` VARCHAR(100) NOT NULL,
                        `POLN` VARCHAR(100) NOT NULL,
                        `RTNO` VARCHAR(100) NOT NULL,
                        `RTLN` VARCHAR(100) NOT NULL,
                        `UNABLE_ACPT_REASON` VARCHAR(500) NULL DEFAULT NULL,
                        `ACPT_DATE` DATE NULL DEFAULT NULL,
                        `UPDATE_USER` VARCHAR(100) NOT NULL,
                        `UPDATE_USER_ID` VARCHAR(50) NOT NULL,
                        `UPDATE_USER_DEPT` VARCHAR(50) NOT NULL,
                        `UPDATE_TIME` DATETIME NOT NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")
            
    ##create tables for ASSET_PMCS_INFOS
    table = config.mysql["table-asset_pmcs_infos"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        `PURNO` VARCHAR(50) NOT NULL,
                        `COMPANY` VARCHAR(50) NULL DEFAULT NULL,
                        `APPLICATION_DATE` DATE NULL DEFAULT NULL,
                        `APPLICANT_NAME` VARCHAR(50) NULL DEFAULT NULL,
                        `APPLICANT_EMPNO` VARCHAR(50) NULL DEFAULT NULL,
                        `APPLICANT_DEPT` VARCHAR(50) NULL DEFAULT NULL,
                        `APPLICANT_MGR_NAME` VARCHAR(50) NULL DEFAULT NULL,
                        `APPLICANT_MGR_EMPNO` VARCHAR(50) NULL DEFAULT NULL,
                        `IDLE_COUNT` INT(11) NULL DEFAULT NULL,
                        PRIMARY KEY (`PURNO`)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")

    ##create tables for ASSET_EMPS_INFO
    table = config.mysql["table-asset_emps_info"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        `emplid` VARCHAR(500) NOT NULL,
                        `site` VARCHAR(500) NULL DEFAULT NULL,
                        `name` VARCHAR(500) NULL DEFAULT NULL,
                        `name_a` VARCHAR(500) NULL DEFAULT NULL,
                        `deptid` VARCHAR(500) NULL DEFAULT NULL,
                        `email_address_a` VARCHAR(500) NULL DEFAULT NULL,
                        PRIMARY KEY (`emplid`)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")
            
    ##create tables for ASSET_EMPS_ORG_INFO
    table = config.mysql["table-asset_emps_org_info"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        `deptid` VARCHAR(500) NOT NULL,
                        `cohead_dept` VARCHAR(500) NULL DEFAULT NULL,
                        `managerid` VARCHAR(500) NULL DEFAULT NULL,
                        `tree_level_num` VARCHAR(500) NULL DEFAULT NULL,
                        `deptMgrId` VARCHAR(500) NULL DEFAULT NULL,
                        `divMgrId` VARCHAR(500) NULL DEFAULT NULL,
                        PRIMARY KEY (`emplid`)
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")

    ##create tables for ASSET_WARRANTY
    table = config.mysql["table-asset_warranty"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        PONO VARCHAR(20),
                        IMPN VARCHAR(15),
                        PRIMARY KEY (PONO, IMPN),
                        WARRANTY INT(11) NULL,
                        UDATE DATE NULL
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")

    ##create tables for ASSET_ENGINEER_MAINTAINED
    table = config.mysql["table-asset_engineer_maintained"]
    print(f"set up table : {table}")
    try:
        cursor.execute(f"SELECT 1 FROM {table} LIMIT 1;")
        print(f"table {table} exists.")
    except pymysql.err.ProgrammingError as e:
        if e.args[0]==1147:
            print(e.args)
            # sql for create table
            sql = f"""CREATE TABLE {table} (
                        ASSETS_NO VARCHAR(15),
                        ASID VARCHAR(15),
                        PRIMARY KEY (ASSETS_NO, ASID),
                        ENGINEER VARCHAR(20),
                        UDATE DATE
                    )"""
            cursor.execute(sql)
            print(f"table: {table} created successfully.")
        else:
            print(f"table: {table} created unsuccessfully.")