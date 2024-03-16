# 3 environments: DEV, QAS, PRD
mode = "DEV"

# MySQL DEV settings
mysql_DEV = {"host": "mysql", "port": 3306, "user": "foo-dev", "password": "mypwd"}
# MySQL QAS settings
mysql_QAS = {"host": "11.22.33.45", "port": 3306, "user": "foo-qas", "password": "mypwd"}
# MySQL PRD settings
mysql_PRD = {"host": "11.22.33.46", "port": 3306, "user": "foo-prd", "password": "mypwd"}

# MySQL common settings
mysql = {"database": "mydb",
         "table-1": "MYSQL_TABLE_NAME_1",
         "table-2": "MYSQL_TABLE_NAME_2",
        }

mysql_cmds = {"insert_table-1": f"""
                    INSERT INTO MYSQL_TABLE_NAME_1 (COLUMN1, COLUMN2, COLUMN3, COLUMN4, COLUMN5) 
                    VALUES (%(COLUMN1)s,%(COLUMN2)s,%(COLUMN3)s,%(COLUMN4)s,%(COLUMN5)s)
                    ON DUPLICATE KEY 
                    UPDATE COLUMN2=VALUES(COLUMN2), COLUMN3=VALUES(COLUMN3), COLUMN4=VALUES(COLUMN4), COLUMN5=VALUES(COLUMN5);
              """,
              "insert_table-2": f"""
                    INSERT INTO MYSQL_TABLE_NAME_2 (COLUMN1, COLUMN2, COLUMN3) 
                    VALUES (%(COLUMN1)s,%(COLUMN2)s,%(COLUMN3)s)
                    ON DUPLICATE KEY 
                    UPDATE COLUMN2=VALUES(COLUMN2), COLUMN3=VALUES(COLUMN3);
              """,
             }

# AIO Redis settings for job scheduler using arq
aio_redis_DEV = {"host": "redis", "port": 6379}
aio_redis_QAS = {"host": "11.22.33.42", "port": 6379}
aio_redis_PRD = {"host": "11.22.33.43", "port": 6379}


### Data sources are from various databases such as PostgreSQL and Oracle
# PostgreSQL settings
postgresql = {"host-1": "11.22.33.47", "port-1": "5566", "user-1": "foo-1", "password-1": "pwd-1", "database-1": "postdb",
              "host-2": "11.22.33.48", "port-2": "5577", "user-1": "foo-2", "password-1": "pwd-2", "database-1": "postdb",
             }

# Oracle settings
oracle = {"host-1": "11.22.33.49", "port-1": "1234", "user-1": "foo-1", "password-1": "pwd-1", "database-1": "DB1",
          "host-2": "11.22.33.50", "port-1": "1235", "user-2": "foo-2", "password-2": "pwd-2", "database-2": "DB2",
         }

# Elasticsearch settings
elasticsearch = {"host": "11.22.33.51", "port": 9200}
