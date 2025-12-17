import logging
from logging.handlers import TimedRotatingFileHandler
from os import makedirs

from settings import ENVIRONMENT, LOG_DIR, LOG_DURATION, LOG_FILE

makedirs(LOG_DIR, exist_ok=True)

error_level = logging.DEBUG
if ENVIRONMENT == 'TESTING':
    error_level = logging.ERROR
elif ENVIRONMENT == 'PRODUCTION':
    error_level = logging.INFO

rotating_handler: TimedRotatingFileHandler = TimedRotatingFileHandler(
    f'{LOG_DIR}/{LOG_FILE}.log',
    when='midnight', # Rotate at midnight
    interval=1, # Every 1 day
    backupCount=LOG_DURATION, # Keep last 7 days
    utc=True,
)
rotating_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
rotating_handler.setLevel(error_level)

logger = logging.getLogger(__name__)
logger.setLevel(error_level)
logger.propagate = False 
logger.addHandler(rotating_handler)
