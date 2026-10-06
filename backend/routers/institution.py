from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from backend.models.schemas import InstitutionAnalyticsResponse
from backend.services.institution_analytics import generate_institution_analytics

router = APIRouter(prefix="/api/institution", tags=["Institution Analytics"])

@router.get("/analytics", response_model=InstitutionAnalyticsResponse)
async def get_institution_analytics(
    institution: Optional[str] = Query("IIT Madras", description="University or Institution Name"),
    department: Optional[str] = Query("Computer Science & Engineering", description="Department Name")
):
    try:
        return generate_institution_analytics(institution_name=institution, department=department)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate institution analytics: {str(e)}")
