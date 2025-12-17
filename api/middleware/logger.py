
import json
from typing import Optional
from fastapi import Request, Response
from fastapi.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from log import logger
from settings import LOG_ALLOWED_METHODS, LOG_RESPONSE, LOG_REQUEST, LOG_PROTECTED_PATHS

class RequestResponseLogger(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        method: str = request.method
        path: str = request.url.path
        client_ip: Optional[str] = request.client.host if request.client else ''
        
        if LOG_REQUEST and method in LOG_ALLOWED_METHODS:
            content_type: str = request.headers.get('Content-Type', '')
            body: object = await request.json()
            logger.info(f'[REQUEST]<[SRC]{client_ip}> :{method}-{path}')
            if path not in LOG_PROTECTED_PATHS and content_type.lower() == 'application/json':
                logger.info(f'[PAYLOAD]{json.dumps(body, separators=(',', ':'))}')

        response: Response= await call_next(request)
        if LOG_RESPONSE and response.headers.get('Content-Type', '').lower() == 'application/json':
            status_code = response.status_code
            body = [section async for section in response.body_iterator] # type: ignore
            response.body_iterator = iterate_in_threadpool(iter(body)) # type: ignore
            logger.info(f'[RESPONSE]{status_code}:{body[0].decode()}')

        return response
