from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Site, SiteDetection, Technology
from app.schemas.site import SiteOut, SiteWithDetections
from app.schemas.detection import DetectionOut

router = APIRouter(prefix="/api/sites", tags=["sites"])


@router.get("", response_model=list[SiteOut])
async def list_sites(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    q: str = Query(None),
    sort: str = Query("tech_count"),
    db: AsyncSession = Depends(get_db),
):
    """List all scanned sites with pagination and search."""
    query = select(Site)

    if q:
        query = query.where(Site.domain.ilike(f"%{q}%"))

    if sort == "tech_count":
        query = query.order_by(Site.tech_count.desc())
    elif sort == "recent":
        query = query.order_by(Site.last_scanned_at.desc())
    elif sort == "domain":
        query = query.order_by(Site.domain)
    else:
        query = query.order_by(Site.tech_count.desc())

    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    return [SiteOut.model_validate(s) for s in result.scalars().all()]


@router.get("/recent", response_model=list[SiteOut])
async def recent_sites(
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """Most recently scanned sites."""
    query = (
        select(Site)
        .where(Site.tech_count > 0)
        .order_by(Site.last_scanned_at.desc())
        .limit(limit)
    )
    result = await db.execute(query)
    return [SiteOut.model_validate(s) for s in result.scalars().all()]


@router.get("/{domain}", response_model=SiteWithDetections)
async def get_site(domain: str, db: AsyncSession = Depends(get_db)):
    """Get site detail with all detections."""
    domain = domain.lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]

    result = await db.execute(select(Site).where(Site.domain == domain))
    site = result.scalar_one_or_none()

    if not site:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"Site {domain} not found")

    det_result = await db.execute(
        select(SiteDetection, Technology)
        .join(Technology, SiteDetection.tech_id == Technology.id)
        .where(SiteDetection.site_id == site.id)
    )

    detections = [
        DetectionOut(
            tech_id=d.id,
            tech_name=t.name,
            tech_slug=t.slug,
            category=t.category,
            website=t.website,
            description=t.description,
            version=d.version,
            confidence=d.confidence or 1.0,
            evidence=d.evidence,
        )
        for d, t in det_result.all()
    ]

    site_out = SiteWithDetections.model_validate(site)
    site_out.detections = detections
    return site_out
