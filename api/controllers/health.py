'''Healthcheck module'''

from fastapi import APIRouter, status


healthRouter: APIRouter = APIRouter()

@healthRouter.get('', status_code=status.HTTP_200_OK)
async def healthcheck():
    return {'status': 'UP'}
