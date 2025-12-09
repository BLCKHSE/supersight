from fastapi import FastAPI

from controllers import (
    healthRouter,
)

def main() -> FastAPI:
    app: FastAPI = FastAPI()

    app.include_router(prefix='/api/health', router=healthRouter)

    return app

app: FastAPI = main()
