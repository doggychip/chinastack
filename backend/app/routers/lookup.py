from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Site, Technology, SiteDetection
from app.schemas.detection import LookupRequest, LookupResponse, DetectionOut
from app.crawler.scanner import scan_url, normalize_url, extract_domain

router = APIRouter(prefix="/api", tags=["lookup"])

CACHE_HOURS = 24


@router.post("/lookup", response_model=LookupResponse)
async def lookup_url(req: LookupRequest, db: AsyncSession = Depends(get_db)):
    """Scan a URL on demand. Returns cached results if scanned < 24h ago."""
    url = normalize_url(req.url)
    domain = extract_domain(url)

    # Check cache
    result = await db.execute(select(Site).where(Site.domain == domain))
    existing_site = result.scalar_one_or_none()

    if existing_site and existing_site.last_scanned_at:
        last_scan = datetime.fromisoformat(existing_site.last_scanned_at)
        if datetime.utcnow() - last_scan < timedelta(hours=CACHE_HOURS):
            # Return cached results
            det_result = await db.execute(
                select(SiteDetection, Technology)
                .join(Technology, SiteDetection.tech_id == Technology.id)
                .where(SiteDetection.site_id == existing_site.id)
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
            return LookupResponse(
                domain=existing_site.domain,
                url=existing_site.url,
                title=existing_site.title,
                icp_number=existing_site.icp_number,
                status_code=existing_site.status_code,
                response_time_ms=existing_site.response_time_ms,
                tech_count=len(detections),
                detections=detections,
                cached=True,
            )

    # Fresh scan
    scan = await scan_url(url)

    if scan.error and not scan.detections:
        raise HTTPException(status_code=502, detail=f"Failed to scan {domain}: {scan.error}")

    # Upsert site
    now = datetime.utcnow().isoformat()
    if existing_site:
        existing_site.url = scan.url
        existing_site.title = scan.title
        existing_site.meta_description = scan.meta_description
        existing_site.icp_number = scan.icp_number
        existing_site.server_header = scan.server_header
        existing_site.status_code = scan.status_code
        existing_site.response_time_ms = scan.response_time_ms
        existing_site.html_size_bytes = scan.html_size_bytes
        existing_site.last_scanned_at = now
        existing_site.scan_count = (existing_site.scan_count or 0) + 1
        existing_site.tech_count = len(scan.detections)
        existing_site.updated_at = now
        site = existing_site

        # Clear old detections
        old_dets = await db.execute(
            select(SiteDetection).where(SiteDetection.site_id == site.id)
        )
        for od in old_dets.scalars().all():
            await db.delete(od)
    else:
        import uuid
        site = Site(
            id=uuid.uuid4().hex[:16],
            domain=domain,
            url=scan.url,
            title=scan.title,
            meta_description=scan.meta_description,
            icp_number=scan.icp_number,
            server_header=scan.server_header,
            status_code=scan.status_code,
            response_time_ms=scan.response_time_ms,
            html_size_bytes=scan.html_size_bytes,
            last_scanned_at=now,
            scan_count=1,
            tech_count=len(scan.detections),
        )
        db.add(site)

    await db.flush()

    # Insert detections
    detections_out = []
    for det in scan.detections:
        tech_result = await db.execute(
            select(Technology).where(Technology.slug == det["slug"])
        )
        tech = tech_result.scalar_one_or_none()
        if not tech:
            continue

        import uuid
        sd = SiteDetection(
            id=uuid.uuid4().hex[:16],
            site_id=site.id,
            tech_id=tech.id,
            confidence=det.get("confidence", 1.0),
            evidence=det.get("evidence", "")[:200],
        )
        db.add(sd)

        detections_out.append(DetectionOut(
            tech_id=tech.id,
            tech_name=tech.name,
            tech_slug=tech.slug,
            category=tech.category,
            website=tech.website,
            description=tech.description,
            confidence=det.get("confidence", 1.0),
            evidence=det.get("evidence", "")[:200],
        ))

    await db.commit()

    return LookupResponse(
        domain=domain,
        url=scan.url,
        title=scan.title,
        icp_number=scan.icp_number,
        status_code=scan.status_code,
        response_time_ms=scan.response_time_ms,
        tech_count=len(detections_out),
        detections=detections_out,
        cached=False,
    )


@router.get("/lookup/{domain}", response_model=LookupResponse)
async def get_cached_lookup(domain: str, db: AsyncSession = Depends(get_db)):
    """Get cached results for a domain."""
    domain = domain.lower().strip()
    if domain.startswith("www."):
        domain = domain[4:]

    result = await db.execute(select(Site).where(Site.domain == domain))
    site = result.scalar_one_or_none()

    if not site:
        raise HTTPException(status_code=404, detail=f"No scan results for {domain}")

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

    return LookupResponse(
        domain=site.domain,
        url=site.url,
        title=site.title,
        icp_number=site.icp_number,
        status_code=site.status_code,
        response_time_ms=site.response_time_ms,
        tech_count=len(detections),
        detections=detections,
        cached=True,
    )
