from motor.motor_asyncio import AsyncIOMotorClient

from store.core.config import settings


class MongoClient:
    client: AsyncIOMotorClient = None


db = MongoClient()


async def connect_to_mongo():
    """Create database connection"""
    db.client = AsyncIOMotorClient(settings.DATABASE_URL)


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()


def get_database():
    """Get database instance"""
    return db.client[settings.DATABASE_NAME]


def get_collection(collection_name: str):
    """Get collection instance"""
    return get_database()[collection_name]
