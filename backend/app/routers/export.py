import csv
import io
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Site, Technology, SiteDetection

router = APIRouter(prefix="/api/export", tags=["export"])


@router.get("/sites")
async def export_sites_csv(
    q: str = Query(None),
    tech: str = Query(None, description="Filter by technology slug"),
    category: str = Query(None, description="Filter by technology category"),
    db: AsyncSession = Depends(get_db),
):
    """Export scanned sites as CSV. Optionally filter by technology or category."""
    query = select(Site)

    if tech:
        query = (
            query.join(SiteDetection, Site.id == SiteDetection.site_id)
            .join(Technology, SiteDetection.tech_id == Technology.id)
            .where(Technology.slug == tech)
        )
    elif category:
        query = (
            query.join(SiteDetection, Site.id == SiteDetection.site_id)
            .join(Technology, SiteDetection.tech_id == Technology.id)
            .where(Technology.category == category)
        )

    if q:
        query = query.where(Site.domain.ilike(f"%{q}%"))

    query = query.order_by(Site.tech_count.desc()).distinct()
    result = await db.execute(query)
    sites = result.scalars().all()

    # For each site, get its technologies
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "domain", "url", "title", "icp_number", "tech_count",
        "technologies", "categories", "status_code", "response_time_ms",
        "last_scanned_at",
    ])

    for site in sites:
        det_result = await db.execute(
            select(Technology.name, Technology.category)
            .join(SiteDetection, Technology.id == SiteDetection.tech_id)
            .where(SiteDetection.site_id == site.id)
        )
        techs = det_result.all()
        tech_names = "; ".join(t[0] for t in techs)
        cat_names = "; ".join(sorted(set(t[1] for t in techs)))

        writer.writerow([
            site.domain,
            site.url,
            site.title or "",
            site.icp_number or "",
            site.tech_count,
            tech_names,
            cat_names,
            site.status_code or "",
            site.response_time_ms or "",
            site.last_scanned_at or "",
        ])

    output.seek(0)
    filename = "chinastack-sites"
    if tech:
        filename += f"-{tech}"
    elif category:
        filename += f"-{category}"
    filename += ".csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get("/technologies")
async def export_technologies_csv(
    category: str = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Export technology adoption data as CSV."""
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

    query = query.order_by(func.coalesce(count_sub.c.site_count, 0).desc())
    result = await db.execute(query)

    total_sites_result = await db.execute(select(func.count()).select_from(Site))
    total_sites = total_sites_result.scalar() or 1

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["name", "slug", "category", "site_count", "market_share_pct", "website", "description"])

    for row in result.all():
        tech = row[0]
        count = row[1]
        pct = round(count / total_sites * 100, 1)
        writer.writerow([
            tech.name, tech.slug, tech.category, count, pct,
            tech.website or "", tech.description or "",
        ])

    output.seek(0)
    filename = f"chinastack-technologies{'-' + category if category else ''}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
