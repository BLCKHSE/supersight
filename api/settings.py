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
LOG_ALLOWED_METHODS: list[str] = getenv('LOG_ALLOWED_METHODS', '').split(',')
LOG_FILE: str = getenv('LOG_FILE', 'supersight')
LOG_DIR: str = '.logs'
LOG_DURATION: int = int(getenv('LOG_DURATION', 7))
LOG_PROTECTED_PATHS: list[str] = getenv('LOG_PROTECTED_PATHS', '').split(',')
LOG_RESPONSE: bool = bool(getenv('LOG_RESPONSE', 'True'))
LOG_REQUEST: bool = bool(getenv('LOG_REQUEST', 'True'))
