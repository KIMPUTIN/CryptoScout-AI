
# backend/api/routes_rankings.py

import hashlib
import json

from fastapi import APIRouter, Response, Request, Query
from fastapi.responses import JSONResponse

from services.ranking_service import (
    get_short_term,
    get_long_term,
    get_low_risk,
    get_high_growth,
    get_top_opportunities
)

router = APIRouter(prefix="/rankings", tags=["Rankings"])


# =====================================================
# ETag Helper
# =====================================================

def etag_response(request: Request, data):

    body = json.dumps(data, sort_keys=True, default=str)

    etag = hashlib.md5(body.encode()).hexdigest()

    client_etag = request.headers.get("if-none-match")

    if client_etag == etag:
        return Response(status_code=304)

    response = JSONResponse(content=data)

    response.headers["ETag"] = etag
    response.headers["Cache-Control"] = "public, max-age=60"

    return response


# =====================================================
# ENDPOINTS
# =====================================================

@router.get("/short-term")
def short_term(
    request: Request,
    profile: str = "balanced",
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):

    data = get_short_term(profile, limit, offset)

    return etag_response(request, data)


@router.get("/long-term")
def long_term(
    request: Request,
    profile: str = "balanced",
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):

    data = get_long_term(profile, limit, offset)

    return etag_response(request, data)


@router.get("/low-risk")
def low_risk(
    request: Request,
    profile: str = "balanced",
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):

    data = get_low_risk(profile, limit, offset)

    return etag_response(request, data)


@router.get("/high-growth")
def high_growth(
    request: Request,
    profile: str = "balanced",
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):

    data = get_high_growth(profile, limit, offset)

    return etag_response(request, data)


@router.get("/opportunities")
def opportunities(
    request: Request,
    limit: int = Query(10, le=50)
):

    projects = get_short_term(limit=200)

    data = get_top_opportunities(projects, limit)

    return etag_response(request, data)


@router.get("/")
def rankings(
    request: Request,
    profile: str = "balanced",
    limit: int = Query(20, le=100),
    offset: int = Query(0)
):

    data = get_short_term(profile, limit, offset)

    return etag_response(request, data)