from fastapi import APIRouter, HTTPException
from database.repositories.calculation_repository import CalculationRepository
from models.calculation import CalculationModel
import base64
from io import BytesIO
from .utils import analyze_image
from schema import ImageData
from PIL import Image
from datetime import datetime

router = APIRouter()

@router.post("")
async def run(data: ImageData):
    try:
        # Process image as before
        image_data = base64.b64decode(data.image.split(",")[1])
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        
        # Create calculation model
        calculation = CalculationModel(
            image_data=data.image,
            responses=responses,
            dict_of_vars=data.dict_of_vars
        )
        
        # Store in database
        calculation_id = await CalculationRepository.create(calculation)
        
        return {
            "message": "Image processed",
            "data": responses,
            "calculation_id": calculation_id,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_history(limit: int = 10):
    calculations = await CalculationRepository.get_recent(limit)
    return {"calculations": [calc.dict(by_alias=True) for calc in calculations]}

@router.put("/{calculation_id}/notes")
async def update_notes(calculation_id: str, notes: str):
    success = await CalculationRepository.update_notes(calculation_id, notes)
    if not success:
        raise HTTPException(status_code=404, detail="Calculation not found")
    return {"message": "Notes updated successfully"}