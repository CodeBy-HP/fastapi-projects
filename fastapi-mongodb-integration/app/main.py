# main.py
from fastapi import FastAPI, HTTPException
from app.models import Item
from app.database import get_collection
from bson import ObjectId

app = FastAPI()
items_collection = get_collection("items")


# Helper to convert MongoDB document to dict
def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "description": item.get("description"),
        "price": item["price"],
    }


@app.post("/items", response_model=dict)
async def create_item(item: Item):
    item_dict = item.model_dump()
    result = await items_collection.insert_one(item_dict)
    new_item = await items_collection.find_one({"_id": result.inserted_id})
    return item_helper(new_item)


@app.get("/items", response_model=list[dict])
async def get_items():
    items_cursor = items_collection.find()
    items = await items_cursor.to_list(length=100)  # limit to 100 for example
    return [item_helper(item) for item in items]
