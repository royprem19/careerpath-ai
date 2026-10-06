from fastapi import APIRouter, HTTPException
from backend.models.schemas import GapAnalysisRequest, GapAnalysisResponse
from backend.services.gap_analyzer import compute_gap
from backend.routers.roles import get_role

router = APIRouter()

@router.post("/api/analysis/gap", response_model=GapAnalysisResponse)
async def analyze_gap(request: GapAnalysisRequest):
    try:
        role = await get_role(request.target_role_id)
        gap = compute_gap(
            user_skills=request.user_skills,
            role_essential_skills=role.essential_skills,
            role_optional_skills=role.optional_skills,
            role_title=role.title,
            role_category=role.category or ""
        )
        return gap
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))
