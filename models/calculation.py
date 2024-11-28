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