from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_password: str
    database_username: str
    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
print(settings.database_password)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI CRUD API!"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)