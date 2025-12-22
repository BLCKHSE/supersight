from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from controllers import (
    accountsRouter,
    ecommRouter,
    healthRouter,
)
from middleware.logger import RequestResponseLogger
from utils.exceptions import InvalidInputException


def main() -> FastAPI:
    app: FastAPI = FastAPI()

    app.include_router(prefix='/api/health', router=healthRouter)
    app.include_router(prefix='/api/accounts', router=accountsRouter)
    app.include_router(prefix='/api/ecommerce', router=ecommRouter)

    return app

app: FastAPI = main()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)
app.add_middleware(RequestResponseLogger)

@app.exception_handler(RequestValidationError)
async def handle_validation_exception(request: Request, ex: RequestValidationError):
    errors: dict[str, str] = {
        '.'.join(err['loc'][(2 if len(err['loc']) > 2 else 1):]) : err['msg']
        for err in ex._errors
    }
    return JSONResponse(status_code=400, content=errors)

@app.exception_handler(InvalidInputException)
async def handle_invalid_input_exception(request: Request, ex: InvalidInputException):
    return JSONResponse(status_code=400, content={ex.field: ex.message})
