"""Rescan all existing sites with updated signatures.

Re-fetches each site and runs the new detection engine against it.
Replaces old detections with new ones.

Usage:
    python3 -m app.rescan
    python3 -m app.rescan --concurrency 5
"""

import asyncio
import argparse
import logging
import uuid
from datetime import datetime

from sqlalchemy import select, delete
from app.database import async_session, init_db
from app.models import Technology, Site, SiteDetection
from app.crawler.scanner import scan_url
from app.crawler.detectors import load_signatures
from app.seed import seed_technologies

logger = logging.getLogger("chinastack.rescan")


async def rescan_all(concurrency: int = 3, delay: float = 1.0):
    """Re-scan all existing sites with updated signatures."""
    await init_db()
    await seed_technologies()

    # Load all sites
    async with async_session() as db:
        result = await db.execute(select(Site).order_by(Site.domain))
        sites = result.scalars().all()
        total = len(sites)
        logger.info(f"Rescanning {total} sites with {len(load_signatures())} signatures")

    success = 0
    failed = 0
    semaphore = asyncio.Semaphore(concurrency)

    async def rescan_one(i: int, site_domain: str, site_url: str, site_id: str):
        nonlocal success, failed
        async with semaphore:
            logger.info(f"[{i+1}/{total}] Rescanning {site_domain}...")
            try:
                scan = await scan_url(site_url)
                now = datetime.utcnow().isoformat()

                async with async_session() as db:
                    # Update site info
                    result = await db.execute(select(Site).where(Site.id == site_id))
                    site = result.scalar_one_or_none()
                    if not site:
                        return

                    site.title = scan.title or site.title
                    site.meta_description = scan.meta_description or site.meta_description
                    site.icp_number = scan.icp_number or site.icp_number
                    site.server_header = scan.server_header
                    site.status_code = scan.status_code
                    site.response_time_ms = scan.response_time_ms
                    site.html_size_bytes = scan.html_size_bytes
                    site.last_scanned_at = now
                    site.scan_count = (site.scan_count or 0) + 1
                    site.tech_count = len(scan.detections)
                    site.updated_at = now

                    # Delete old detections
                    await db.execute(
                        delete(SiteDetection).where(SiteDetection.site_id == site_id)
                    )

                    # Insert new detections
                    for det in scan.detections:
                        tech_result = await db.execute(
                            select(Technology).where(Technology.slug == det["slug"])
                        )
                        tech = tech_result.scalar_one_or_none()
                        if not tech:
                            continue

                        sd = SiteDetection(
                            id=uuid.uuid4().hex[:16],
                            site_id=site_id,
                            tech_id=tech.id,
                            confidence=det.get("confidence", 1.0),
                            evidence=(det.get("evidence", "") or "")[:200],
                        )
                        db.add(sd)

                    await db.commit()

                status = f"{len(scan.detections)} techs"
                if scan.icp_number:
                    status += f", ICP: {scan.icp_number}"
                logger.info(f"  OK  {site_domain} -> {status}")
                success += 1

            except Exception as e:
                logger.error(f"  FAIL {site_domain}: {e}")
                failed += 1

            await asyncio.sleep(delay)

    # Build task list from site data
    site_data = []
    async with async_session() as db:
        result = await db.execute(select(Site).order_by(Site.domain))
        for site in result.scalars().all():
            site_data.append((site.domain, site.url, site.id))

    # Process in batches
    batch_size = concurrency
    for batch_start in range(0, total, batch_size):
        batch = site_data[batch_start:batch_start + batch_size]
        tasks = [
            rescan_one(batch_start + j, domain, url, sid)
            for j, (domain, url, sid) in enumerate(batch)
        ]
        await asyncio.gather(*tasks)

    logger.info(f"Rescan complete: {success} updated, {failed} failed out of {total}")


async def main():
    parser = argparse.ArgumentParser(description="Rescan all sites with updated signatures")
    parser.add_argument("--concurrency", type=int, default=3)
    parser.add_argument("--delay", type=float, default=1.0)
    args = parser.parse_args()

    await rescan_all(concurrency=args.concurrency, delay=args.delay)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main())
