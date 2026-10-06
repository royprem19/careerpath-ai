from fastapi import APIRouter, HTTPException
from backend.models.schemas import RoadmapRequest, RoadmapResponse
from backend.services.roadmap_generator import generate_roadmap
from backend.database import get_supabase

router = APIRouter()

@router.post("/api/roadmap", response_model=RoadmapResponse)
async def create_roadmap(request: RoadmapRequest):
    supabase = get_supabase()
    courses = []
    
    if supabase:
        try:
            resp = supabase.table("courses").select("*").in_("skill_name", request.missing_skills).execute()
            if resp.data:
                courses = resp.data
        except Exception:
            pass
            
    try:
        roadmap_entries = generate_roadmap(request.missing_skills, courses)
        return RoadmapResponse(entries=roadmap_entries)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
