from typing import List
from fastapi import FastAPI, HTTPException, status, Depends, Response
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI CRUD API!"}

app.include_router(post.router)
app.include_router(user.router)