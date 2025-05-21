from pydantic import BaseModel
from fastapi import FastAPI, HTTPException

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