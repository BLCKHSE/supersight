
from os import getenv
from typing import cast, get_args

from schemas.literals import Environment


ENVIRONMENT: Environment = cast(
    Environment,
    getenv('ENVIRONMENT', 'DEVELOPMENT') 
    if getenv('ENVIRONMENT', 'DEVELOPMENT') not in get_args(Environment) 
    else 'DEVELOPMENT'
)

# DATABASE
DATABASE_URL: str = getenv('DATABASE_URL', '')

# LOGGING
LOG_FILE: str = getenv('LOG_FILE', 'supersight')
LOG_DIR: str = '.logs'
LOG_DURATION: int = int(getenv('LOG_DURATION', 7))
