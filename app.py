import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations.fastapi import setup_dishka

from src.ioc import container
from src.controllers.api_routes import router


async def main():
    app = FastAPI(
        title="apo-web-api",
        docs_url="/api/docs",
        openapi_url='/api/openapi.json'
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router, prefix='/api')
    setup_dishka(container, app)

    return app


if __name__ == '__main__':
    uvicorn.run(main, host='0.0.0.0', port=8000)
