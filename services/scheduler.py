'''
Scheduler
'''
import datetime as dt
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
# import os
import logging

# Configuração básica de logging
hoje = dt.datetime.today().strftime("%Y-%m-%d")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(f"app-{hoje}.log"),
              logging.StreamHandler()])

logger = logging.getLogger(__name__)

# Initialize a SQLAlchemyJobStore with SQLite database
jobstores = {'default': MemoryJobStore()}

# Initialize an AsyncIOScheduler with the jobstore
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone='America/Sao_Paulo')


# This is a scheduled job that will run every 10 seconds.
@scheduler.scheduled_job('cron', hour=4, minute=0, second=0)
def sch_importar_omie():
    print('ola')
    return
