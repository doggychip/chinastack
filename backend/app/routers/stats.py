from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Site, Technology, SiteDetection

router = APIRouter(prefix="/api/stats", tags=["stats"])

CATEGORIES = {
    "analytics": "数据分析",
    "payment": "支付",
    "cdn": "CDN",
    "framework_fe": "前端框架",
    "framework_be": "后端框架",
    "cms": "CMS",
    "ecommerce": "电商平台",
    "cloud": "云服务",
    "miniprogram": "小程序",
    "advertising": "广告",
    "customer_service": "客服",
    "map": "地图",
    "security": "安全",
    "font": "字体",
    "video": "视频",
    "social": "社交",
    "server": "服务器",
    "javascript": "JS库",
    "ui": "UI组件库",
    "tag_manager": "标签管理",
    "hosting": "托管",
    "email": "邮件",
    "other": "其他",
}


@router.get("/overview")
async def get_overview(db: AsyncSession = Depends(get_db)):
    """Total sites, techs, categories."""
    site_count = (await db.execute(select(func.count()).select_from(Site))).scalar() or 0
    tech_count = (await db.execute(select(func.count()).select_from(Technology))).scalar() or 0
    detection_count = (await db.execute(select(func.count()).select_from(SiteDetection))).scalar() or 0

    cat_result = await db.execute(
        select(Technology.category, func.count())
        .group_by(Technology.category)
    )
    categories = [
        {"key": row[0], "label": CATEGORIES.get(row[0], row[0]), "tech_count": row[1]}
        for row in cat_result.all()
    ]

    return {
        "total_sites": site_count,
        "total_technologies": tech_count,
        "total_detections": detection_count,
        "categories": sorted(categories, key=lambda x: x["tech_count"], reverse=True),
    }


@router.get("/top-technologies")
async def get_top_technologies(
    limit: int = Query(20, ge=1, le=2000),
    db: AsyncSession = Depends(get_db),
):
    """Top N most common technologies across all scanned sites."""
    query = (
        select(
            Technology.name,
            Technology.slug,
            Technology.category,
            func.count(SiteDetection.site_id).label("site_count"),
        )
        .join(SiteDetection, Technology.id == SiteDetection.tech_id)
        .group_by(Technology.id)
        .order_by(func.count(SiteDetection.site_id).desc())
        .limit(limit)
    )

    result = await db.execute(query)
    total_sites = (await db.execute(select(func.count()).select_from(Site))).scalar() or 1

    return [
        {
            "name": row[0],
            "slug": row[1],
            "category": row[2],
            "category_label": CATEGORIES.get(row[2], row[2]),
            "count": row[3],
            "percentage": round(row[3] / total_sites * 100, 1),
        }
        for row in result.all()
    ]


@router.get("/category/{category}")
async def get_category_stats(category: str, db: AsyncSession = Depends(get_db)):
    """Market share within a category."""
    if category not in CATEGORIES:
        raise HTTPException(status_code=404, detail=f"Unknown category: {category}")

    query = (
        select(
            Technology.name,
            Technology.slug,
            func.count(SiteDetection.site_id).label("site_count"),
        )
        .join(SiteDetection, Technology.id == SiteDetection.tech_id)
        .where(Technology.category == category)
        .group_by(Technology.id)
        .order_by(func.count(SiteDetection.site_id).desc())
    )

    result = await db.execute(query)
    rows = result.all()

    total = sum(r[2] for r in rows) or 1

    return {
        "category": category,
        "category_label": CATEGORIES[category],
        "technologies": [
            {
                "name": row[0],
                "slug": row[1],
                "count": row[2],
                "percentage": round(row[2] / total * 100, 1),
            }
            for row in rows
        ],
    }
