from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
from .routes import pdf_routes
from .config import FRONTEND_ORIGIN
from .utils.cleanup import cleanup_task

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pdf_routes.router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(cleanup_task())
