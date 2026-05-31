from typing import Optional

from fastapi import FastAPI, responses, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class Item(BaseModel):
    mutta: str
    done: bool = True
    rate: Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="!m00sx@123",
            cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as e:
        print("Database connection failed")
        print(e)
        time.sleep(2)

item_test = [ {"mutta": "m1", "done": True, "rate": 1}, {"mutta": "m2", "done": False, "rate": 2}, {"mutta": "m3", "done": True, "rate": 3} ]

@app.get("/")
async def root():
    return {"message": item_test}

@app.post("/items/")
def create_item(item: Item):
    item.rate = randrange(1, 10)
    item_test.append(item.dict())
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
            item_test[i] = item.dict()
            return item_test[i]
    raise HTTPException(status_code=404, detail="Item not found")