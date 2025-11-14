from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import create_document, get_documents
from schemas import Product, Order

app = FastAPI(title="Minimalist Clothing Store API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

@app.get("/", response_model=Message)
async def root():
    return {"message": "Store API is running"}

@app.get("/test", response_model=Message)
async def test():
    # quick DB check: list products (no error if empty)
    _ = await get_documents("product", {}, limit=1)
    return {"message": "DB connection OK"}

@app.get("/products", response_model=List[Product])
async def list_products():
    items = await get_documents("product", {}, limit=100)
    # cast to Product compatible dicts
    return [Product(**{k: v for k, v in i.items() if k != "id"}).model_dump() for i in items]

@app.post("/products", response_model=Product)
async def create_product(product: Product):
    created = await create_document("product", product.model_dump())
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create product")
    created.pop("id", None)
    return Product(**created)

@app.post("/orders")
async def create_order(order: Order):
    created = await create_document("order", order.model_dump())
    if not created:
        raise HTTPException(status_code=500, detail="Failed to create order")
    created.pop("id", None)
    return created
