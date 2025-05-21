from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

router = APIRouter()

# --- Модели ---

class WatchItem(BaseModel):
    movie_id: str
    watched_at: datetime
    rating: Optional[float] = None

class Preferences(BaseModel):
    genres: List[str]
    actors: List[str]
    directors: List[str]

class DeviceInfo(BaseModel):
    platform: str
    os: str
    app_version: str

class Location(BaseModel):
    country: str
    city: Optional[str] = None

class Context(BaseModel):
    time_of_day: str
    mood_tag: Optional[str] = None

class RecommendationRequest(BaseModel):
    user_id: str
    session_id: str
    timestamp: datetime
    watch_history: List[WatchItem]
    preferences: Preferences
    device_info: DeviceInfo
    location: Location
    context: Context
    algorithm: Optional[str] = None

class RecommendationItem(BaseModel):
    movie_id: str
    title: str
    score: float
    reason: str

class RecommendationResponse(BaseModel):
    request_id: str
    generated_at: datetime
    recommendations: List[RecommendationItem]
    algorithm_used: Optional[str] = None
    next_refresh_in: int  # seconds

# --- Эндпоинт ---

@router.post("/recommendations", response_model=RecommendationResponse)
async def get_recommendations(req: RecommendationRequest):
    # Тут может быть реальный вызов ML-модуля или проксирование к другому сервису
    print(f"Received recommendation request for user: {req.user_id}")

    fake_results = [
        RecommendationItem(
            movie_id="m321",
            title="Интерстеллар",
            score=0.98,
            reason="Схожа тематика космоса + любимый режиссёр"
        ),
        RecommendationItem(
            movie_id="m654",
            title="Матрица",
            score=0.95,
            reason="Keanu Reeves + киберпанк"
        )
    ]

    return RecommendationResponse(
        request_id="req_987",
        generated_at=datetime.utcnow(),
        recommendations=fake_results,
        algorithm_used=req.algorithm or "default_v1",
        next_refresh_in=3600
    )
