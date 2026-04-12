from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Technology, SiteDetection, Site
from app.schemas.technology import TechnologyOut
from app.schemas.site import SiteOut

router = APIRouter(prefix="/api/technologies", tags=["technologies"])


@router.get("", response_model=list[TechnologyOut])
async def list_technologies(
    category: str = Query(None),
    q: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """List all technologies with site counts."""
    # Subquery for site counts
    count_sub = (
        select(SiteDetection.tech_id, func.count(SiteDetection.site_id).label("site_count"))
        .group_by(SiteDetection.tech_id)
        .subquery()
    )

    query = (
        select(Technology, func.coalesce(count_sub.c.site_count, 0).label("site_count"))
        .outerjoin(count_sub, Technology.id == count_sub.c.tech_id)
    )

    if category:
        query = query.where(Technology.category == category)
    if q:
        query = query.where(Technology.name.ilike(f"%{q}%"))

    query = query.order_by(func.coalesce(count_sub.c.site_count, 0).desc())

    result = await db.execute(query)
    techs = []
    for row in result.all():
        tech = row[0]
        count = row[1]
        t = TechnologyOut.model_validate(tech)
        t.site_count = count
        techs.append(t)
    return techs


@router.get("/{slug}", response_model=TechnologyOut)
async def get_technology(slug: str, db: AsyncSession = Depends(get_db)):
    """Get technology detail."""
    result = await db.execute(select(Technology).where(Technology.slug == slug))
    tech = result.scalar_one_or_none()
    if not tech:
        raise HTTPException(status_code=404, detail=f"Technology {slug} not found")

    count_result = await db.execute(
        select(func.count()).where(SiteDetection.tech_id == tech.id)
    )
    count = count_result.scalar() or 0

    out = TechnologyOut.model_validate(tech)
    out.site_count = count
    return out


@router.get("/{slug}/sites", response_model=list[SiteOut])
async def get_technology_sites(
    slug: str,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Get all sites using a specific technology."""
    result = await db.execute(select(Technology).where(Technology.slug == slug))
    tech = result.scalar_one_or_none()
    if not tech:
        raise HTTPException(status_code=404, detail=f"Technology {slug} not found")

    offset = (page - 1) * per_page
    site_query = (
        select(Site)
        .join(SiteDetection, Site.id == SiteDetection.site_id)
        .where(SiteDetection.tech_id == tech.id)
        .order_by(Site.tech_count.desc())
        .offset(offset)
        .limit(per_page)
    )

    sites_result = await db.execute(site_query)
    return [SiteOut.model_validate(s) for s in sites_result.scalars().all()]
