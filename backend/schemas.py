from pydantic import BaseModel, Field
from typing import Optional, List

# Schema definitions: each model corresponds to a collection (lowercased name)

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    slug: str = Field(..., min_length=1, max_length=140)
    price: float = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=1000)
    images: List[str] = Field(default_factory=list)
    sizes: List[str] = Field(default_factory=list)
    colors: List[str] = Field(default_factory=list)
    in_stock: bool = True
    featured: bool = False
    category: Optional[str] = None

class OrderItem(BaseModel):
    product_id: str
    name: str
    price: float
    quantity: int = Field(..., ge=1)
    size: Optional[str] = None
    color: Optional[str] = None

class Order(BaseModel):
    items: List[OrderItem]
    subtotal: float
    shipping: float
    total: float
    currency: str = "USD"
    email: Optional[str] = None
    status: str = "pending"
