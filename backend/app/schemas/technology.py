from pydantic import BaseModel
from typing import Optional


class TechnologyOut(BaseModel):
    id: str
    name: str
    slug: str
    category: str
    subcategory: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    icon_url: Optional[str] = None
    site_count: int = 0

    model_config = {"from_attributes": True}
