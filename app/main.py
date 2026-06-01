from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Item(BaseModel):
    mutta: str
    done: bool = True
    rate: Optional[int] = None

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="fastapi",
        user="postgres",
        password="!m00sx@123",
        cursor_factory=RealDictCursor,
        connect_timeout=3)

item_test = [ {"mutta": "m1", "done": True, "rate": 1}, {"mutta": "m2", "done": False, "rate": 2}, {"mutta": "m3", "done": True, "rate": 3} ]

@app.get("/")
async def root():
    return {"message": item_test}

@app.get("/posts")
def get_posts():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM posts")
            posts = cursor.fetchall()
        return {"data": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

 
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    return {"data": post}

@app.post("/postss", status_code=status.HTTP_201_CREATED)
def create_post_sqlalchemy(post: Post, db: Session = Depends(get_db)):
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *",
                (post.title, post.content))
            new_post = cursor.fetchone()
            conn.commit()
        return {"data": new_post}
    except Exception as e:
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn:
            conn.close()

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404, detail=f"Post with id {id} was not found")
    post.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return {"data": post}

@app.post("/items/")
def create_item(item: Item):
    next_rate = max([x["rate"] for x in item_test if x["rate"] is not None], default=0) + 1
    item.rate = next_rate
    item_test.append(item.model_dump())
    return item_test

@app.get("/items/{rate}")
def read_item(rate: int):
    for item in item_test:
        if item["rate"] == rate:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{rate}")
def update_item(rate:int, item: Item):
    for i in range(len(item_test)):
        if item_test[i]["rate"] == rate:
            item.rate = rate
            item_test[i] = item.model_dump()
            return item_test[i]
    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts} 