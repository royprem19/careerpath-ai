from fastapi import APIRouter, HTTPException
from backend.models.schemas import RecommendationRequest, RecommendationResponse
from backend.services.recommender import recommend_roles
from backend.routers.roles import list_roles
from typing import List

router = APIRouter()

@router.post("/api/recommendations", response_model=List[RecommendationResponse])
async def get_recommendations(request: RecommendationRequest):
    try:
        roles = await list_roles()
        roles_dict_list = [
            {
                "id": r.id,
                "title": r.title,
                "category": r.category or "Technology",
                "description": r.description or "",
                "essential_skills": r.essential_skills,
                "optional_skills": r.optional_skills
            } for r in roles
        ]
        
        recs = recommend_roles(
            user_skills=request.user_skills,
            user_education=request.user_education,
            user_experience=request.user_experience,
            all_roles=roles_dict_list,
            raw_text=request.raw_text or ""
        )
        return recs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
