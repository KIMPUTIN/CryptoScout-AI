
from fastapi import APIRouter, Depends
from api.dependencies import require_pro
from services.explanation_service import generate_trending_explanation
from services.ai_service import analyze_project  # adjust if different
from models.schemas import AIRequest  # adjust if your schema path differs
from repositories.project_repository import (
    increment_analysis_count,
    reset_daily_count_if_needed
)

DAILY_LIMIT = 15

router = APIRouter(prefix="/ai", tags=["AI"])


@router.get("/explain/{symbol}")
def explain(symbol: str): #, user=Depends(require_pro)): ------
    return generate_trending_explanation(symbol)


@router.post("/analyze")
async def analyze(request: AIRequest, user=Depends(require_pro)):
    user = reset_daily_count_if_needed(user)

    if user.get("daily_analysis_count", 0) >= DAILY_LIMIT:
        raise HTTPException(
            status_code=403,
            detail="Daily analysis limit reached"
        )

    return analyze_project(request.symbol)

    result = run_full_analysis(request, user)

    increment_analysis_count(user["id"])

    return result
    