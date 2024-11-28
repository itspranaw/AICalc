from motor.motor_asyncio import AsyncIOMotorClient
from constants import MONGODB_URL, DB_NAME

class DatabaseConnection:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    async def connect(cls):
        if cls.client is None:
            cls.client = AsyncIOMotorClient(MONGODB_URL)
            cls.db = cls.client[DB_NAME]
            try:
                await cls.client.admin.command('ping')
                print("Successfully connected to MongoDB!")
            except Exception as e:
                print(f"Could not connect to MongoDB: {e}")
                raise e

    @classmethod
    async def close(cls):
        if cls.client:
            await cls.client.close()
            cls.client = None
            cls.db = None
            print("MongoDB connection closed")

    @classmethod
    def get_db(cls):
        return cls.db

# models/calculation.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Dict, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

class CalculationModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    image_data: str
    responses: List[Dict[str, Any]]
    notes: str = ""
    dict_of_vars: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True