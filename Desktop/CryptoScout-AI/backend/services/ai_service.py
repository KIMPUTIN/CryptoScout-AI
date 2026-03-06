# backend/services/ai_service.py

import json
import logging
from typing import Dict, Any

from openai import OpenAI

from core.config import OPENAI_API_KEY, AI_MODEL, AI_TIMEOUT, AI_MAX_RETRIES
from services.scoring_service import fallback_analysis
from core.redis_client import cache_get, cache_set
from core.circuit_breaker import ai_circuit_breaker

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


# =====================================================
# QUALIFICATION FILTER
# =====================================================

def qualifies_for_ai(project: Dict[str, Any]) -> bool:
    """
    Determine whether project is worth AI analysis.
    Prevents wasting tokens on low-value coins.
    """

    try:
        market_cap = float(project.get("market_cap") or 0)
        volume = float(project.get("volume_24h") or 0)
        change_24h = abs(float(project.get("price_change_24h") or 0))

        if market_cap < 20_000_000:
            return False

        if volume < 2_000_000:
            return False

        if change_24h < 2:
            return False

        return True

    except Exception:
        return False


# =====================================================
# PRE ANALYSIS CACHE CHECK
# =====================================================

if not ai_circuit_breaker.can_execute():
    logger.warning("AI circuit open — using fallback")
    return fallback_analysis(project)

def analyze_project(project):

    symbol = project.get("symbol")

    cache_key = f"ai_analysis:{symbol}"

    cached = cache_get(cache_key)

    if cached:
        return cached


# =====================================================
# AI ANALYSIS
# =====================================================

def analyze_project(project):

    symbol = project.get("symbol")
    cache_key = f"ai_analysis:{symbol}"

    cached = cache_get(cache_key)
    if cached:
        return cached

    if not ai_circuit_breaker.can_execute():
        return fallback_analysis(project)

    try:

        # call OpenAI
        response = client.chat.completions.create(...)

        parsed = json.loads(response)

        score = ...
        confidence = ...

        result = {
            "score": score,
            "verdict": parsed["verdict"],
            "confidence": confidence
        }

        cache_set(cache_key, result, 3600)

        ai_circuit_breaker.record_success()

        return result

    except Exception:

        ai_circuit_breaker.record_failure()

        return fallback_analysis(project)

    prompt = f"""
Return ONLY JSON with:
score (0-100),
verdict (STRONG BUY, BUY, HOLD, AVOID),
confidence (0-1).

Score rules:
90-100 = Exceptional momentum and liquidity
75-89 = Strong bullish signals
60-74 = Moderate upside potential
45-59 = Neutral
0-44 = Weak fundamentals

DATA:
Name: {project.get("name")}
Symbol: {project.get("symbol")}
Market Cap: {project.get("market_cap")}
24h Volume: {project.get("volume_24h")}
24h Change: {project.get("price_change_24h")}
7d Change: {project.get("price_change_7d")}
Rank: {project.get("market_cap_rank")}
"""

    for attempt in range(AI_MAX_RETRIES):

        try:
            response = client.chat.completions.create(
                model=AI_MODEL,
                messages=[
                    {"role": "system", "content": "Return ONLY valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=200,
                timeout=AI_TIMEOUT,
                response_format={"type": "json_object"}
            )

            result = response.choices[0].message.content
            parsed = json.loads(result)

            score = max(0, min(100, float(parsed["score"])))
            confidence = max(0, min(1, float(parsed["confidence"])))

            ai_circuit_breaker.record_success()

            result = {
                "score": score,
                "verdict": parsed["verdict"],
                "confidence": confidence
            }

            cache_set(cache_key, result, 3600)

            return result

        except Exception as e:

            ai_circuit_breaker.record_failure()

            logger.warning("AI attempt failed: %s", e)

    logger.error("AI failed — using fallback scoring")

    return fallback_analysis(project)


# =====================================================
# AI SUMMARY GENERATION
# =====================================================

def generate_summary(project: Dict[str, Any]) -> str:
    """
    Generate short explanation for frontend.
    """

    if not client:
        return "AI summary unavailable."

    prompt = f"""
Explain briefly why {project['name']} ({project['symbol']})
is trending based on:

Market Cap
24h Change
7d Change
Volume
AI Score

Keep it under 100 words.
"""

    try:

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "Be concise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=150,
            timeout=15
        )

        return response.choices[0].message.content.strip()

    except Exception:

        return "AI summary unavailable."


# =====================================================
# AI ENGINE HEALTH
# =====================================================

def ai_engine_health() -> Dict[str, Any]:
    """
    Health check used by monitoring endpoints.
    """

    return {
        "status": "ok" if OPENAI_API_KEY else "degraded",
        "openai_key_loaded": bool(OPENAI_API_KEY),
        "engine": "CryptoScout AI"
    }


def pre_analyze_projects(projects, limit=100):
    """
    Pre-compute AI analysis for top projects
    so results are cached before users request them.
    """

    analyzed = []

    for project in projects[:limit]:

        try:

            result = analyze_project(project)

            project["ai_score"] = result.get("score")
            project["ai_verdict"] = result.get("verdict")
            project["ai_confidence"] = result.get("confidence")

            analyzed.append(project)

        except Exception:
            continue

    return analyzed