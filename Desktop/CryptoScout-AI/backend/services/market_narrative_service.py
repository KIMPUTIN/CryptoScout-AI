
# backend/services/market_narrative_service.py

import logging
from typing import List, Dict

from openai import OpenAI
from core.config import OPENAI_API_KEY, AI_MODEL
from core.redis_client import cache_set

logger = logging.getLogger(__name__)

client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None


def generate_market_narrative(projects: List[Dict], signals: List[Dict]) -> str:
    """
    Generate a short AI narrative describing market conditions.
    """

    if not client:
        return "AI narrative unavailable."

    # summarize top movers
    top_projects = sorted(
        projects,
        key=lambda x: x.get("combined_score", 0),
        reverse=True
    )[:5]

    project_summary = "\n".join(
        f"{p.get('symbol')} | Score {p.get('combined_score')} | AI {p.get('ai_score')}"
        for p in top_projects
    )

    signal_summary = "\n".join(
        f"{s.get('type')} — {s.get('symbol')}"
        for s in signals[:5]
    )

    prompt = f"""
You are a crypto market analyst.

Summarize current market conditions in under 120 words.

Top ranked assets:
{project_summary}

Detected signals:
{signal_summary}

Explain:
- overall market sentiment
- key trends
- notable assets
"""

    try:

        response = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": "Be concise and analytical."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=200
        )

        narrative = response.choices[0].message.content.strip()

        cache_set("market_narrative", narrative, 300)

        return narrative

    except Exception as e:

        logger.error("Narrative generation failed: %s", e)

        return "AI narrative unavailable."