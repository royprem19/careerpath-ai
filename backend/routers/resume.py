from fastapi import APIRouter, UploadFile, File, HTTPException, Header
from typing import Optional
from backend.services.resume_parser import parse_resume
from backend.services.skill_extractor import extract_skills, extract_education, extract_experience, extract_certifications
from backend.services.skill_normalizer import normalize_skills, normalize_skill
from backend.services.auth_service import get_current_user
from backend.models.schemas import ResumeUploadResponse, SkillNormalizeRequest, SkillNormalizeResponse

router = APIRouter()

@router.post("/api/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(None)
):
    # Enforce authentication: User must be signed in with a valid JWT token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, 
            detail="Authentication required: Please sign in or register before uploading your resume."
        )

    token = authorization.split("Bearer ", 1)[1].strip()
    user = get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired session token. Please sign in again."
        )

    try:
        content = await file.read()
        text = parse_resume(content, file.filename or "")
        
        raw_skills = extract_skills(text)
        skills = normalize_skills(raw_skills)
        education = extract_education(text)
        experience = extract_experience(text)
        certifications = extract_certifications(text)
        
        # Uncertainty & Quality Assessment
        text_len = len(text.strip())
        is_scanned = text_len < 80
        warning_msg = None
        
        if is_scanned and len(skills) == 0:
            confidence = 0.1
            warning_msg = "Low text density detected. This file appears to be a scanned image or photo without selectable text. Please manually add your skills below."
        elif len(skills) < 3:
            confidence = round(max(0.2, len(skills) * 0.25), 2)
            warning_msg = f"Only {len(skills)} skill(s) detected. To ensure accurate role recommendations, please verify or add your skills below."
        else:
            confidence = round(min(1.0, 0.6 + (len(skills) * 0.04)), 2)
        
        return ResumeUploadResponse(
            skills=skills,
            education=education,
            experience=experience,
            certifications=certifications,
            raw_text=text,
            confidence_score=confidence,
            is_scanned_or_low_text=is_scanned,
            warning_message=warning_msg
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/skills/normalize", response_model=SkillNormalizeResponse)
async def api_normalize_skills(request: SkillNormalizeRequest):
    return SkillNormalizeResponse(normalized_skills=normalize_skills(request.skills))
