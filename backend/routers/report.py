from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from backend.services.report_generator import generate_pdf_report
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter()

class ReportRequest(BaseModel):
    user_profile: Dict[str, Any]
    gap_analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    roadmap: List[Dict[str, Any]]

@router.post("/api/report/pdf")
async def get_pdf_report(request: ReportRequest):
    try:
        pdf_bytes = generate_pdf_report(
            user_profile=request.user_profile,
            gap_analysis=request.gap_analysis,
            recommendations=request.recommendations,
            roadmap=request.roadmap
        )
        return Response(
            content=pdf_bytes, 
            media_type="application/pdf", 
            headers={"Content-Disposition": "attachment; filename=report.pdf"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
