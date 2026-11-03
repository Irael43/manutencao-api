from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import router
from app.services import load_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Iniciando API...")
    load_model()
    yield
    print("🛑 Encerrando API...")

app = FastAPI(
    title="Manutenção Preditiva API",
    description="API para predição de falhas em equipamentos industriais",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router)