"""Bulk scanner — crawl thousands of Chinese websites.

Usage:
    python3 -m app.bulk_scan                    # scan all lists
    python3 -m app.bulk_scan --list ecommerce   # scan specific list
    python3 -m app.bulk_scan --file urls.txt    # scan from file (one URL per line)
"""

import asyncio
import argparse
import logging
import uuid
from datetime import datetime

from sqlalchemy import select
from app.database import async_session, init_db
from app.models import Technology, Site, SiteDetection
from app.crawler.scanner import scan_url, extract_domain, normalize_url
from app.crawler.detectors import load_signatures
from app.seed import seed_technologies

logger = logging.getLogger("chinastack.bulk")

# ── Domain lists by category ──────────────────────────────────────────────

ECOMMERCE = [
    # 电商
    "taobao.com", "tmall.com", "jd.com", "pinduoduo.com", "vip.com",
    "suning.com", "dangdang.com", "amazon.cn", "kaola.com", "yanxuan.netease.com",
    "mogujie.com", "meilishuo.com", "yihaodian.com", "gome.com.cn", "jumei.com",
    "xiaohongshu.com", "dewu.com", "youzan.com", "weidian.com", "kuajingmaihuo.com",
    "1688.com", "alibaba.com", "made-in-china.com", "globalsources.com",
    "dhgate.com", "aliexpress.com",
]

FINANCE = [
    # 金融/支付
    "eastmoney.com", "xueqiu.com", "snowball.com", "10jqka.com.cn",
    "lufax.com", "ant.com", "alipay.com", "tenpay.com",
    "cmbc.com.cn", "icbc.com.cn", "ccb.com.cn", "boc.cn", "abchina.com",
    "cmbchina.com", "bankcomm.com", "psbc.com", "spdb.com.cn",
    "cib.com.cn", "pingan.com", "cpic.com.cn", "citicbank.com",
    "futu.com", "longbridge.com", "tiger.com",
]

TECH = [
    # 科技/互联网
    "baidu.com", "alibaba.com", "tencent.com", "bytedance.com", "meituan.com",
    "didi.com", "xiaomi.com", "huawei.com", "oppo.com", "vivo.com",
    "oneplus.com", "realme.com", "honor.com", "lenovo.com.cn", "zte.com.cn",
    "sensetime.com", "megvii.com", "cambricon.com", "horizon.ai",
    "dji.com", "tuya.com", "hikvision.com", "dahua.com",
    "iflytek.com", "baichuan-ai.com", "moonshot.cn", "zhipuai.cn",
    "minimax.chat", "01.ai",
]

MEDIA = [
    # 媒体/内容
    "bilibili.com", "douyin.com", "kuaishou.com", "weibo.com",
    "zhihu.com", "douban.com", "jianshu.com", "csdn.net",
    "36kr.com", "huxiu.com", "geekpark.net", "sspai.com",
    "iqiyi.com", "youku.com", "mgtv.com", "le.com",
    "ximalaya.com", "lizhi.fm", "qingting.fm",
    "163.com", "qq.com", "sohu.com", "sina.com", "ifeng.com",
    "thepaper.cn", "caixin.com", "yicai.com", "jiemian.com",
    "toutiao.com", "infoq.cn", "oschina.net", "juejin.cn",
    "segmentfault.com", "v2ex.com",
]

TRAVEL = [
    # 旅游/出行
    "ctrip.com", "qunar.com", "fliggy.com", "mafengwo.cn",
    "tuniu.com", "ly.com", "booking.com", "airbnb.cn",
    "didi.com", "amap.com", "map.baidu.com",
    "12306.cn", "ceair.com", "csair.com", "airchina.com.cn",
]

EDUCATION = [
    # 教育
    "xueersi.com", "koolearn.com", "huohua.cn", "fenbi.com",
    "zhangmen.com", "vipkid.com", "zuoyebang.com", "yuanfudao.com",
    "mooc.cn", "icourse163.org", "xuetangx.com", "cnmooc.org",
    "chaoxing.com", "zhihuishu.com", "coursera.org",
]

REALESTATE = [
    # 房产
    "ke.com", "lianjia.com", "anjuke.com", "fang.com",
    "ziroom.com", "danke.com", "5i5j.com",
]

LIFESTYLE = [
    # 本地生活
    "ele.me", "meituan.com", "dianping.com", "koubei.com",
    "daojia.com", "58.com", "ganji.com",
]

AUTO = [
    # 汽车
    "nio.cn", "xpeng.com", "li.auto", "byd.com",
    "autohome.com.cn", "yiche.com", "dongchedi.com",
    "tesla.cn", "geely.com", "changan.com.cn", "gwm.com.cn",
    "zeekrlife.com",
]

CLOUD_SAAS = [
    # 云/SaaS
    "aliyun.com", "cloud.tencent.com", "huaweicloud.com",
    "qiniu.com", "upyun.com", "ucloud.cn", "ksyun.com",
    "feishu.cn", "dingtalk.com", "wecom.work",
    "teambition.com", "ones.ai", "tapd.cn",
    "worktile.com", "coding.net", "gitee.com",
    "shimo.im", "mubu.com", "yuque.com",
    "sensorsdata.cn", "growingio.com", "volcengine.com",
]

GOVT_EDU = [
    # 政府/机构
    "gov.cn", "moe.gov.cn", "miit.gov.cn", "mof.gov.cn",
    "pbc.gov.cn", "csrc.gov.cn", "ndrc.gov.cn",
    "tsinghua.edu.cn", "pku.edu.cn", "fudan.edu.cn",
    "sjtu.edu.cn", "zju.edu.cn", "ustc.edu.cn",
    "nju.edu.cn", "whu.edu.cn", "hust.edu.cn",
]

GAMING = [
    # 游戏
    "163.com", "qq.com", "mihoyo.com", "lilith.com",
    "xd.com", "taptap.cn", "4399.com", "7k7k.com",
    "37.com", "yoozoo.com", "bilibili.com",
]

ALL_LISTS = {
    "ecommerce": ECOMMERCE,
    "finance": FINANCE,
    "tech": TECH,
    "media": MEDIA,
    "travel": TRAVEL,
    "education": EDUCATION,
    "realestate": REALESTATE,
    "lifestyle": LIFESTYLE,
    "auto": AUTO,
    "cloud_saas": CLOUD_SAAS,
    "govt_edu": GOVT_EDU,
    "gaming": GAMING,
}


def deduplicate(urls: list[str]) -> list[str]:
    """Deduplicate by domain, preserving order."""
    seen = set()
    result = []
    for u in urls:
        domain = extract_domain(normalize_url(u))
        if domain not in seen:
            seen.add(domain)
            result.append(u)
    return result


async def scan_and_save(url: str, db) -> bool:
    """Scan a single URL and save results. Returns True on success."""
    domain = extract_domain(normalize_url(url))

    # Skip if already scanned
    result = await db.execute(select(Site).where(Site.domain == domain))
    if result.scalar_one_or_none():
        return True

    try:
        scan = await scan_url(url)
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
        status = f"{len(scan.detections)} techs"
        if scan.icp_number:
            status += f", ICP: {scan.icp_number}"
        if scan.error:
            status += f" (warning: {scan.error[:50]})"
        logger.info(f"  OK  {domain} -> {status}")
        return True

    except Exception as e:
        logger.error(f"  FAIL {domain}: {e}")
        await db.rollback()
        return False


async def bulk_scan(domains: list[str], delay: float = 1.5, concurrency: int = 3):
    """Scan a list of domains with rate limiting and concurrency."""
    domains = deduplicate(domains)
    total = len(domains)
    success = 0
    skipped = 0
    failed = 0

    logger.info(f"Starting bulk scan: {total} domains, delay={delay}s, concurrency={concurrency}")

    semaphore = asyncio.Semaphore(concurrency)

    async def scan_one(i: int, url: str):
        nonlocal success, skipped, failed
        async with semaphore:
            domain = extract_domain(normalize_url(url))

            async with async_session() as db:
                # Check if already scanned
                result = await db.execute(select(Site).where(Site.domain == domain))
                if result.scalar_one_or_none():
                    skipped += 1
                    logger.info(f"[{i+1}/{total}] SKIP {domain} (already scanned)")
                    return

                logger.info(f"[{i+1}/{total}] Scanning {domain}...")
                ok = await scan_and_save(url, db)
                if ok:
                    success += 1
                else:
                    failed += 1

            await asyncio.sleep(delay)

    # Process in batches to respect rate limits
    batch_size = concurrency
    for batch_start in range(0, total, batch_size):
        batch = domains[batch_start:batch_start + batch_size]
        tasks = [scan_one(batch_start + j, url) for j, url in enumerate(batch)]
        await asyncio.gather(*tasks)

    logger.info(f"Bulk scan complete: {success} new, {skipped} skipped, {failed} failed out of {total}")
    return {"success": success, "skipped": skipped, "failed": failed, "total": total}


async def main():
    parser = argparse.ArgumentParser(description="ChinaStack bulk scanner")
    parser.add_argument("--list", type=str, help="Scan specific list (ecommerce, finance, tech, etc.)")
    parser.add_argument("--file", type=str, help="Scan URLs from a text file (one per line)")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between requests (seconds)")
    parser.add_argument("--concurrency", type=int, default=3, help="Concurrent requests")
    parser.add_argument("--all", action="store_true", help="Scan all built-in lists")
    args = parser.parse_args()

    await init_db()
    await seed_technologies()

    if args.file:
        with open(args.file, "r") as f:
            domains = [line.strip() for line in f if line.strip()]
        logger.info(f"Loaded {len(domains)} URLs from {args.file}")
        await bulk_scan(domains, delay=args.delay, concurrency=args.concurrency)

    elif args.list:
        if args.list not in ALL_LISTS:
            print(f"Unknown list: {args.list}. Available: {', '.join(ALL_LISTS.keys())}")
            return
        domains = ALL_LISTS[args.list]
        logger.info(f"Scanning list: {args.list} ({len(domains)} domains)")
        await bulk_scan(domains, delay=args.delay, concurrency=args.concurrency)

    else:
        # Scan all lists (original + extended + expanded)
        from app.domains_extended import ALL_EXTENDED
        from app.domains_expanded import get_all_expanded_domains
        all_domains = []
        for name, domains in ALL_LISTS.items():
            all_domains.extend(domains)
        for name, domains in ALL_EXTENDED.items():
            all_domains.extend(domains)
        all_domains.extend(get_all_expanded_domains())
        all_domains = deduplicate(all_domains)
        logger.info(f"Scanning ALL lists: {len(all_domains)} unique domains")
        await bulk_scan(all_domains, delay=args.delay, concurrency=args.concurrency)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    asyncio.run(main())
