from pydantic import BaseModel
from typing import Optional


class DetectionOut(BaseModel):
    tech_id: str
    tech_name: str
    tech_slug: str
    category: str
    website: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    confidence: float = 1.0
    evidence: Optional[str] = None

    model_config = {"from_attributes": True}


class LookupRequest(BaseModel):
    url: str


class LookupResponse(BaseModel):
    domain: str
    url: str
    title: Optional[str] = None
    icp_number: Optional[str] = None
    status_code: Optional[int] = None
    response_time_ms: Optional[int] = None
    tech_count: int = 0
    detections: list[DetectionOut] = []
    cached: bool = False
