from pydantic import BaseModel
from typing import Optional


class SiteBase(BaseModel):
    domain: str
    url: str
    title: Optional[str] = None
    meta_description: Optional[str] = None
    icp_number: Optional[str] = None
    icp_entity: Optional[str] = None
    server_header: Optional[str] = None
    status_code: Optional[int] = None
    response_time_ms: Optional[int] = None


class SiteOut(SiteBase):
    id: str
    last_scanned_at: Optional[str] = None
    scan_count: int = 1
    html_size_bytes: Optional[int] = None
    tech_count: int = 0
    created_at: Optional[str] = None

    model_config = {"from_attributes": True}


class SiteWithDetections(SiteOut):
    detections: list["DetectionOut"] = []


from app.schemas.detection import DetectionOut  # noqa: E402
SiteWithDetections.model_rebuild()
