from fastapi import FastAPI
from sqladmin import Admin
from sqladmin_inline import setup_inline_routes
from Admin.auth import AdminAuth
from db import engine
from Admin.interface import *
import os
from db import engine, Base, get_db
from Admin.editor import InstructionEditor
from pathlib import Path

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

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

admin.add_view(InstructionAdmin)
admin.add_view(InstructionEditor)