"""
FastAPI Store API - Aplicação principal
Seguindo padrão da professora Nayanna Nara - DIO.me Store API
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from store.core.config import settings
from store.db.mongo import connect_to_mongo
from store.routers import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events - conectar ao MongoDB na inicialização"""
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    pass


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            version="1.0.0",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH,
            lifespan=lifespan
        )


app = App()
app.include_router(api_router)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Store API is running! 🏪"}
