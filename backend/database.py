import os
from typing import Any, Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "appdb")

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def get_db() -> AsyncIOMotorDatabase:
    global _client, _db
    if _db is None:
        _client = AsyncIOMotorClient(DATABASE_URL)
        _db = _client[DATABASE_NAME]
    return _db

async def create_document(collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
    db = await get_db()
    now = datetime.utcnow()
    doc = {**data, "created_at": now, "updated_at": now}
    result = await db[collection].insert_one(doc)
    created = await db[collection].find_one({"_id": result.inserted_id})
    if created and "_id" in created:
        created["id"] = str(created.pop("_id"))
    return created or {}

async def get_documents(collection: str, filter_dict: Dict[str, Any] | None = None, limit: int = 50) -> List[Dict[str, Any]]:
    db = await get_db()
    cursor = db[collection].find(filter_dict or {}).limit(limit)
    items = []
    async for item in cursor:
        item["id"] = str(item.pop("_id"))
        items.append(item)
    return items
