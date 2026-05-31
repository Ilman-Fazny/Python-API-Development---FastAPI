from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class Item(BaseModel):
    mutta: str
    done: bool = True
    rate: Optional[int] = None

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
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"data": posts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/items/")
def create_item(item: Item):
    item.rate = randrange(1, 10)
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
            item_test[i] = item.model_dump()
            return item_test[i]
    raise HTTPException(status_code=404, detail="Item not found")
