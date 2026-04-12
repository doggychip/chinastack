import asyncio
import json
import os
import uuid
import logging

from sqlalchemy import select
from app.database import async_session, init_db
from app.models import Technology, Site, SiteDetection
from app.crawler.scanner import scan_url, extract_domain
from app.crawler.detectors import load_signatures

logger = logging.getLogger("chinastack.seed")

SEED_URLS = [
    "https://www.baidu.com",
    "https://www.taobao.com",
    "https://www.tmall.com",
    "https://www.jd.com",
    "https://www.bilibili.com",
    "https://www.zhihu.com",
    "https://www.douyin.com",
    "https://www.weibo.com",
    "https://www.163.com",
    "https://www.qq.com",
    "https://www.sohu.com",
    "https://www.sina.com",
    "https://www.douban.com",
    "https://www.csdn.net",
    "https://www.meituan.com",
    "https://www.dianping.com",
    "https://www.xiaomi.com",
    "https://www.huawei.com",
    "https://www.bytedance.com",
    "https://www.pinduoduo.com",
    "https://www.ele.me",
    "https://www.ctrip.com",
    "https://www.iqiyi.com",
    "https://www.youku.com",
    "https://www.aliyun.com",
    "https://cloud.tencent.com",
    "https://www.36kr.com",
    "https://www.jianshu.com",
    "https://www.zhaopin.com",
    "https://www.boss.com",
    "https://www.ximalaya.com",
    "https://www.kuaishou.com",
    "https://www.toutiao.com",
    "https://www.suning.com",
    "https://www.vip.com",
    "https://www.dangdang.com",
    "https://www.eastmoney.com",
    "https://www.snowball.com",
    "https://www.ke.com",
    "https://www.lianjia.com",
    "https://www.nio.cn",
    "https://www.xpeng.com",
    "https://www.mi.com",
    "https://www.oppo.com",
    "https://www.vivo.com",
    "https://www.dji.com",
    "https://www.sensetime.com",
    "https://www.megvii.com",
    "https://www.geekbang.org",
    "https://www.infoq.cn",
]


async def seed_technologies():
    """Load all technologies from signatures.json into the database."""
    signatures = load_signatures()

    async with async_session() as db:
        for tech in signatures:
            result = await db.execute(
                select(Technology).where(Technology.slug == tech["slug"])
            )
            if result.scalar_one_or_none():
                continue

            t = Technology(
                id=uuid.uuid4().hex[:16],
                name=tech["name"],
                slug=tech["slug"],
                category=tech["category"],
                website=tech.get("website"),
                description=tech.get("description"),
            )
            db.add(t)

        await db.commit()
        logger.info(f"Seeded {len(signatures)} technologies")


async def seed_sites():
    """Scan top Chinese sites. Runs with delays to be polite."""
    async with async_session() as db:
        for i, url in enumerate(SEED_URLS):
            domain = extract_domain(url)

            # Skip if already scanned
            result = await db.execute(select(Site).where(Site.domain == domain))
            if result.scalar_one_or_none():
                logger.info(f"[{i+1}/{len(SEED_URLS)}] Skipping {domain} (already scanned)")
                continue

            logger.info(f"[{i+1}/{len(SEED_URLS)}] Scanning {domain}...")

            try:
                scan = await scan_url(url)

                from datetime import datetime
                now = datetime.utcnow().isoformat()

                site = Site(
                    id=uuid.uuid4().hex[:16],
                    domain=scan.domain,
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

                for det in scan.detections:
                    tech_result = await db.execute(
                        select(Technology).where(Technology.slug == det["slug"])
                    )
                    tech = tech_result.scalar_one_or_none()
                    if not tech:
                        continue

                    sd = SiteDetection(
                        id=uuid.uuid4().hex[:16],
                        site_id=site.id,
                        tech_id=tech.id,
                        confidence=det.get("confidence", 1.0),
                        evidence=(det.get("evidence", "") or "")[:200],
                    )
                    db.add(sd)

                await db.commit()
                logger.info(f"  -> {domain}: {len(scan.detections)} technologies detected")

                if scan.error:
                    logger.warning(f"  -> {domain} had error: {scan.error}")

            except Exception as e:
                logger.error(f"  -> Failed to scan {domain}: {e}")
                await db.rollback()

            # Rate limit: 2 second delay between requests
            await asyncio.sleep(2)

    logger.info("Seed scan complete!")


async def run_seed():
    """Full seed: init DB, load technologies, scan sites."""
    await init_db()
    await seed_technologies()
    await seed_sites()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(run_seed())
