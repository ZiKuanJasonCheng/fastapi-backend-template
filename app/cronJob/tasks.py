import sys

from arq import create_pool, cron
from arq.connections import RedisSettings
from .. import logger, config

from app.cronJob.task.routineTask1 import task1
#from app.cronJob.task.routineTask2 import task2

sys.path.append("/app")

log_filename = "tasks.log"
myLogger = logger.get_logger("tasks", log_filename)
dic_myLogger = {}


async def startup(ctx):
    pass

async def shutdown(ctx):
    pass

# Define our task1 routine to be added to cron_jobs
async def run_routineTask1(ctx):
    if dic_myLogger.get("routineTask1") is not None:
        myLogger = dic_myLogger["routineTask1"]
    else:
        myLogger = logger.get_logger("routineTask1", log_filename)
        dic_myLogger["routineTask1"] = myLogger
    myLogger.info("Running routineTask1...")
    await task1(myLogger)
    myLogger.info("routineTask1 done.")
    return 

# async def run_routineTask2(ctx):
#     if dic_myLogger.get("routineTask2") is not None:
#         myLogger = dic_myLogger["routineTask2"]
#     else:
#         myLogger = logger.get_logger("routineTask2", log_filename)
#         dic_myLogger["routineTask2"] = myLogger
#     myLogger.info("Running routineTask2...")
#     await task2(myLogger)
#     myLogger.info("routineTask2 done.")
#     return 

class WorkerSettings:
    if config.mode == "DEV":
        redis_settings = RedisSettings(
            host=config.aio_redis_DEV["host"],
            port=config.aio_redis_DEV["port"],
            database=0
        )
    elif config.mode == "QAS":
        redis_settings = RedisSettings(
            host=config.aio_redis_QAS["host"],
            port=config.aio_redis_QAS["port"],
            database=0
        )
    else:  # config.mode == "PRD"
        redis_settings = RedisSettings(
            host=config.aio_redis_PRD["host"],
            port=config.aio_redis_PRD["port"],
            database=0
        )
    
    cron_jobs = [
        # Run for every 10 minutes
        #cron(run_routineTask2, minute={10, 20, 30, 40, 50}),

        # Run for every 4 hours
        #cron(run_routineTask3, hour={0, 4, 8, 12, 16, 20}, minute=30),

        ## daily update
        cron(run_routineTask1, hour=1, minute=00),
        #cron(run_routineTask2, hour=2, minute=00),
    ]
    
    on_startup = startup
    on_shutdown = shutdown
