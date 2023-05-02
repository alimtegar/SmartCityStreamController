from fastapi import FastAPI

from .routes import router

def register_module(app: FastAPI):
    app.include_router(router)
