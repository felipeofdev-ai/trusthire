"""Resume optimization endpoints (ATS universal + PDF export)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from ai.router import ai_router
from services.resume_optimizer import ResumeOptimizer, SUPPORTED_ATS, generate_resume_pdf

router = APIRouter(prefix="/resume", tags=["Resume"])
optimizer = ResumeOptimizer()


class ResumeOptimizeRequest(BaseModel):
    resume_text: str = Field(..., min_length=20, max_length=25000)
    job_description: str = Field(..., min_length=20, max_length=25000)
    ats_provider: str = Field(default="generic")
    output_format: str = Field(default="json")  # json | pdf


@router.post("/optimize")
async def optimize_resume(request: ResumeOptimizeRequest):
    provider = request.ats_provider.lower().strip()
    if provider not in SUPPORTED_ATS:
        provider = "generic"

    result = optimizer.optimize(
        resume_text=request.resume_text,
        job_description=request.job_description,
        provider=provider,
    )

    ai_hint = ai_router("resume", request.job_description)

    if request.output_format == "pdf":
        pdf_bytes = generate_resume_pdf(result.optimized_text)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=trusthire_resume_optimized.pdf"},
        )

    if request.output_format != "json":
        raise HTTPException(status_code=400, detail="output_format must be 'json' or 'pdf'")

    return {
        "provider": result.provider,
        "ats_score": result.score,
        "missing_keywords": result.missing_keywords,
        "suggestions": result.suggestions,
        "optimized_text": result.optimized_text,
        "ai": ai_hint,
        "supported_ats": SUPPORTED_ATS,
    }
