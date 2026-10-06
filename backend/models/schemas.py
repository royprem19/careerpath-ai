from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union

class ResumeUploadResponse(BaseModel):
    skills: List[str] = []
    education: List[str] = []
    experience: Dict[str, Any] = {}
    certifications: List[str] = []
    raw_text: str = ""

class SkillNormalizeRequest(BaseModel):
    skills: List[str]

class SkillNormalizeResponse(BaseModel):
    normalized_skills: List[str]

class RoleResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    essential_skills: List[str] = []
    optional_skills: List[str] = []
    avg_salary: Optional[Union[str, float]] = None
    experience_range: Optional[str] = None

class GapAnalysisRequest(BaseModel):
    user_skills: List[str] = Field(default=[], alias="userSkills")
    target_role_id: str = Field(..., alias="targetRoleId")

    model_config = {
        "populate_by_name": True
    }

class GapAnalysisResponse(BaseModel):
    fit_score: float
    essential_coverage: float
    optional_coverage: float
    missing_essential: List[str]
    missing_optional: List[str]
    matched_skills: List[str]
    surplus_skills: List[str]
    total_required: int = 0
    matched_count: int = 0
    why_this_role: Optional[str] = None
    predicted_salary: Optional[str] = None
    skill_velocities: Optional[List[Dict[str, Any]]] = None

class RecommendationRequest(BaseModel):
    user_skills: List[str] = Field(default=[], alias="userSkills")
    user_education: Optional[Union[List[str], List[Dict[str, Any]]]] = Field(default=[], alias="education")
    user_experience: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = Field(default={}, alias="experience")
    raw_text: Optional[str] = ""

    model_config = {
        "populate_by_name": True
    }

class RecommendationResponse(BaseModel):
    role_id: str
    role_title: str
    score: float
    explanation: str

class RoadmapRequest(BaseModel):
    missing_skills: List[str] = Field(default=[], alias="missingSkills")
    preferences: Optional[Dict[str, Any]] = None

    model_config = {
        "populate_by_name": True
    }

class RoadmapEntry(BaseModel):
    week: int
    skill: str
    course: str
    platform: str
    url: Optional[str] = None
    project: str
    duration: str
    is_free: bool = True
    difficulty: str = "Beginner"

class RoadmapResponse(BaseModel):
    entries: List[RoadmapEntry]

class UserProfile(BaseModel):
    skills: List[str] = []
    education: List[str] = []
    experience: Dict[str, Any] = {}
    certifications: List[str] = []

# ==============================================================================
# AUTH & INSTITUTION SCHEMAS
# ==============================================================================
class UserRegisterRequest(BaseModel):
    email: str
    password: str
    user_name: str
    role: str = "candidate"  # "candidate" or "institution_admin"
    institution_name: Optional[str] = "All India Institute of Technology"
    department: Optional[str] = "Computer Science & Engineering"
    graduation_year: Optional[int] = 2026
    skills: Optional[List[str]] = []

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserUpdateRequest(BaseModel):
    user_name: Optional[str] = None
    institution_name: Optional[str] = None
    department: Optional[str] = None
    graduation_year: Optional[int] = None

class UserResponse(BaseModel):
    id: str
    email: str
    user_name: str
    role: str
    institution_name: Optional[str] = None
    department: Optional[str] = None
    graduation_year: Optional[int] = None
    skills: List[str] = []

class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class SkillGapCohortItem(BaseModel):
    skill: str
    students_missing_pct: float
    frequency: int
    industry_demand: str
    priority: str

class CurriculumSubjectAudit(BaseModel):
    subject: str
    alignment_score: float
    gap_summary: str
    industry_benchmark: str

class CurriculumElectiveRecommendation(BaseModel):
    title: str
    duration_weeks: int
    target_skills: List[str]
    impact_pct: float
    rationale: str

class InstitutionAnalyticsResponse(BaseModel):
    institution_name: str
    total_students_analyzed: int
    curriculum_alignment_score: float
    placement_readiness: Dict[str, float]
    top_aggregate_skill_gaps: List[SkillGapCohortItem]
    subject_alignment_audit: List[CurriculumSubjectAudit]
    recommended_electives: List[CurriculumElectiveRecommendation]
