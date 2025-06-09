from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import router
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()  # Initialize MongoDB indexes
    yield  # Let the application run
    print("Shutting down...")  # (Optional) Cleanup actions if needed


app = FastAPI(lifespan=lifespan)

app.include_router(router)
