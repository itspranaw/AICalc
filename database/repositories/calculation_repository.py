from models.calculation import CalculationModel
from database.connection import DatabaseConnection
from typing import List, Optional
from bson import ObjectId

class CalculationRepository:
    @staticmethod
    async def create(calculation: CalculationModel) -> str:
        db = DatabaseConnection.get_db()
        result = await db.calculations.insert_one(calculation.dict(by_alias=True))
        return str(result.inserted_id)

    @staticmethod
    async def get_by_id(calculation_id: str) -> Optional[CalculationModel]:
        db = DatabaseConnection.get_db()
        result = await db.calculations.find_one({"_id": ObjectId(calculation_id)})
        if result:
            return CalculationModel(**result)
        return None

    @staticmethod
    async def get_recent(limit: int = 10) -> List[CalculationModel]:
        db = DatabaseConnection.get_db()
        cursor = db.calculations.find().sort("timestamp", -1).limit(limit)
        return [CalculationModel(**doc) async for doc in cursor]

    @staticmethod
    async def update_notes(calculation_id: str, notes: str) -> bool:
        db = DatabaseConnection.get_db()
        result = await db.calculations.update_one(
            {"_id": ObjectId(calculation_id)},
            {"$set": {"notes": notes}}
        )
        return result.modified_count > 0