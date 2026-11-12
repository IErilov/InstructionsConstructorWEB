from fastapi import FastAPI, Depends
from sqladmin import Admin
from sqladmin_inline import setup_inline_routes
from fastapi.middleware.cors import CORSMiddleware
from Admin.auth import AdminAuth
from db import engine
from Admin.interface import *
import os
from db import engine, Base, get_db
from Admin.editor import InstructionEditor
from pathlib import Path
from Core.Analitics.session import get_anonymous_id
from Core.Analitics.analitics import router as analitics_router
from Admin.analitics import AnalyticsView
from Routers.Instructions import router as instruct_router

SECRET_KEY = os.getenv("SECRET_KEY")
BASE_DIR: Path = Path(__file__).resolve().parent

app = FastAPI(title="ICW")
admin = Admin(
    app,
    engine,
    authentication_backend=AdminAuth(secret_key=SECRET_KEY),
    title="Admin panel",
    templates_dir=str(BASE_DIR / "templates")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:5173",
        "http://127.0.0.1",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analitics_router)
app.include_router(instruct_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

admin.add_view(InstructionAdmin)
admin.add_view(InstructionEditor)
admin.add_view(AnalyticsView)