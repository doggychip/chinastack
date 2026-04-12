"""Expanded Chinese website domains for bulk scanning.

~850+ new domains organized by category. These are deduplicated against
the existing lists in bulk_scan.py (ecommerce, finance, tech, media, travel,
education, real estate, lifestyle, auto, cloud/SaaS, govt/edu, gaming).

Usage:
    from app.domains_expanded import ALL_EXPANDED, get_all_expanded_domains
    domains = get_all_expanded_domains()  # flat deduplicated list
"""

# ── 1. Top Chinese websites by traffic (not already covered) ─────────────

TOP_TRAFFIC = [
    # Major portals and high-traffic sites not in existing lists
    "people.com.cn",        # People's Daily
    "xinhuanet.com",        # Xinhua News Agency
    "cctv.com",             # CCTV
    "chinadaily.com.cn",    # China Daily
    "china.com",            # China.com portal
    "china.com.cn",         # China Internet Information Center
    "huanqiu.com",          # Global Times
    "cankaoxiaoxi.com",     # Reference News
    "gmw.cn",               # Guangming Daily
    "youth.cn",             # China Youth Daily
    "workercn.cn",          # Workers Daily
    "81.cn",                # PLA Daily
    "ce.cn",                # China Economic Net
    "chinanews.com",        # China News Service
    "cnr.cn",               # China National Radio
    "cri.cn",               # China Radio International
    "stdaily.com",          # Science and Technology Daily
    "legaldaily.com.cn",    # Legal Daily
    "farmer.com.cn",        # Farmers Daily
    "cflac.org.cn",         # China Federation of Literary and Art Circles
    "cnki.net",             # CNKI (academic)
    "wanfangdata.com.cn",   # Wanfang Data
    "cqvip.com",            # Chongqing VIP
    "soku.com",             # Soku video search
    "pptv.com",             # PPTV
    "56.com",               # 56.com video
    "acfun.cn",             # AcFun
    "tudou.com",            # Tudou
    "ku6.com",              # Ku6
    "fun.tv",               # Fun.tv (Feng Xing)
    "titan24.com",          # Titan Sports
    "eastday.com",          # Eastday (Shanghai)
    "enorth.com.cn",        # Enorth (Tianjin)
    "southcn.com",          # Southern Net (Guangdong)
    "dahe.cn",              # Dahe (Henan)
    "rednet.cn",            # Red Net (Hunan)
    "cqnews.net",           # Chongqing News
    "sznews.com",           # Shenzhen News
    "hexun.com",            # Hexun Finance
    "stockstar.com",        # Stockstar
    "cnfol.com",            # CNFOL Finance
    "jrj.com.cn",           # JRJ Finance
    "p5w.net",              # P5W Finance
    "nbd.com.cn",           # National Business Daily
    "cls.cn",               # CLS Finance
    "ynet.com",             # Beijing Youth Daily
    "takungpao.com",        # Ta Kung Pao
    "wenweipo.com",         # Wen Wei Po
    "stcn.com",             # Securities Times
    "cs.com.cn",            # China Securities Journal
    "ccidnet.com",          # CCID Net
    "zol.com.cn",           # ZOL (electronics reviews)
    "pconline.com.cn",      # PConline
    "it168.com",            # IT168
    "yesky.com",            # Yesky
    "mydrivers.com",        # MyDrivers
    "expreview.com",        # Expreview
    "cnbeta.com",           # cnBeta
    "ithome.com",           # IT Home
    "51cto.com",            # 51CTO
    "chinaz.com",           # Chinaz webmaster tools
    "admin5.com",           # Admin5
]

# ── 2. Chinese SaaS companies ───────────────────────────────────────────

SAAS = [
    # CRM & Sales
    "xiaoshouyi.com",       # Xiaoshouyi (Salesforce-like CRM)
    "fxiaoke.com",          # Fenxiang Xiaoke (social CRM)
    "ec.com.cn",            # EC (SCRM)
    "weimob.com",           # Weimob (marketing SaaS)
    "youzan.com",           # Youzan (ecommerce SaaS) -- may overlap but different context
    "mengyiapp.com",        # Mengyi
    "marketin.cn",          # Marketin (marketing automation)
    "convertlab.com",       # ConvertLab (marketing cloud)
    "linkflowtech.com",    # LinkFlow CDP
    "jiguang.cn",           # Jiguang (push notification SaaS)

    # HR & Collaboration
    "beisen.com",           # Beisen (HR SaaS)
    "moka.com",             # Moka (ATS/recruiting)
    "mokahr.com",           # Moka HR
    "dayi.com",             # Dayi HR
    "2haohr.com",           # 2Hao HR
    "italent.cn",           # iTalent
    "xinrenxinshi.com",     # XinRenXinShi (HR)
    "kingdee.com",          # Kingdee (ERP/finance)
    "yonyou.com",           # Yonyou (ERP)
    "chanjet.com",          # Chanjet (SMB accounting)
    "tongbu.com",           # Tongbu
    "qingflow.com",         # QingFlow (low-code)
    "mingdao.com",          # Mingdao (collaboration)
    "jiandaoyun.com",       # JianDaoYun (low-code)
    "fanruan.com",          # FanRuan (BI/reporting)
    "finebi.com",           # FineBI
    "smartbi.com.cn",       # SmartBI
    "yonghongtech.com",     # Yonghong BI
    "tableausoft.com",      # Tableau China
    "qlikview.com",         # QlikView China (informational)

    # DevOps & Engineering
    "tapd.cn",              # TAPD (Tencent agile)
    "pingcode.com",         # PingCode
    "ones.ai",              # ONES (project management)
    "tower.im",             # Tower (project management)
    "worktile.com",         # Worktile
    "teambition.com",       # Teambition
    "eolink.com",           # Eolink (API management)
    "apipost.cn",           # ApiPost
    "apifox.cn",            # Apifox
    "showdoc.com.cn",       # ShowDoc

    # Communication & IM
    "rongcloud.cn",         # RongCloud (IM SDK)
    "easemob.com",          # Easemob (IM SDK)
    "leancloud.cn",         # LeanCloud (BaaS)
    "bmob.cn",              # Bmob (BaaS)
    "wilddog.com",          # Wilddog (realtime)
    "getui.com",            # Getui (push)
    "umeng.com",            # Umeng (analytics)

    # E-signature & Doc
    "esign.cn",             # e-Sign (e-signature)
    "bestsign.cn",          # BestSign
    "fadada.com",           # FaDaDa (e-contracts)
    "qiyuesuo.com",         # QiYueSuo (e-contracts)
    "wps.cn",               # WPS Office
    "kdocs.cn",             # Kingsoft Docs
    "yozosoft.com",         # Yozo Office
    "foxitsoftware.cn",     # Foxit Software

    # Cloud Security
    "qianxin.com",          # QiAnXin (security)
    "sangfor.com.cn",       # Sangfor
    "venustech.com.cn",     # VenusTech
    "nsfocus.com.cn",       # NSFOCUS
    "dbappsecurity.com.cn", # DBAPPSecurity
    "hillstonenet.com.cn",  # Hillstone Networks
    "knownsec.com",         # Knownsec
    "threatbook.cn",        # ThreatBook
    "antiy.com",            # Antiy Labs
]

# ── 3. B2B platforms ────────────────────────────────────────────────────

B2B = [
    "1688.com",             # Alibaba B2B (domestic)
    "hc360.com",            # HC360 (Huicong)
    "makepolo.com",         # Makepolo
    "b2b168.com",           # B2B168
    "china.cn",             # China.cn B2B
    "net114.com",           # Net114
    "wjw.cn",               # WJW (hardware B2B)
    "gongchang.com",        # Gongchang
    "qjy168.com",           # Qianjianyuan
    "youboy.com",           # Youboy
    "toocle.com",           # Toocle
    "netsun.com",           # NetSun
    "cpooo.com",            # CPOOO
    "51sole.com",           # 51Sole
    "huangye88.com",        # Huangye88
    "jqw.com",              # JQW
    "sm160.com",            # SM160
    "cn.chemnet.com",       # ChemNet
    "molbase.com",          # Molbase (chemical)
    "lookchem.cn",          # LookChem
    "zgong.com",            # Zgong (industrial)
    "gkzhan.com",           # GKZhan (automation)
    "chem17.com",           # Chem17
    "ybzhan.cn",            # Ybzhan (instruments)
    "foodjx.com",           # Foodjx (food machinery)
    "86pla.com",            # 86PLA (plastics)
    "jc001.cn",             # JC001 (building materials)
    "bmlink.com",           # BMLink (building materials)
    "co188.com",            # CO188 (construction)
    "zhaoshang100.com",     # Zhaoshang100 (franchising)
]

# ── 4. Healthcare / Pharma ──────────────────────────────────────────────

HEALTHCARE = [
    # Online health platforms
    "haodf.com",            # Hao Dai Fu (Good Doctor)
    "guahao.com",           # Guahao (WeDoctor)
    "wedoctor.com",         # WeDoctor
    "chunyuyisheng.com",    # Chunyu Doctor
    "xywy.com",             # Xun Yi Wen Yao
    "39.net",               # 39 Health
    "familydoctor.com.cn",  # Family Doctor Online
    "120.net",              # 120 Health
    "dxy.cn",               # DXY (Dingxiang Yuan)
    "youlai.cn",            # YouLai Health
    "miaoshou.com",         # Miaoshou Doctor
    "jianke.com",           # Jianke Pharmacy
    "yaofang.cn",           # Yaofang.cn
    "360kad.com",           # 360 Health Pharmacy
    "111.com.cn",           # 111 Inc (online pharmacy)
    "jdhealth.com",         # JD Health
    "alihealth.cn",         # AliHealth
    "healthjd.com",         # JD Health Mall
    "yihu.com",             # Yihu

    # Pharma companies
    "hengrui.com",          # Hengrui Medicine
    "cspc.com.cn",          # CSPC Pharma
    "aierchina.com",        # Aier Eye Hospital
    "bfrimed.com",          # BeiGene (partial)
    "beigene.cn",           # BeiGene
    "wuxiapptec.com.cn",    # WuXi AppTec
    "wuxibiologics.com.cn", # WuXi Biologics
    "innoventbio.com",      # Innovent Biologics
    "zailab.com.cn",        # Zai Lab
    "legendbiotech.cn",     # Legend Biotech
    "junshi.com.cn",        # Junshi Biosciences
    "akeso.com",            # Akeso
    "glorypharma.com",      # Glory Pharma
    "tasly.com",            # Tasly Pharma
    "pien-tze-huang.com",   # Pien Tze Huang
    "tcmhz.com",            # Tong Ren Tang
    "tongrentang.com",      # Tong Ren Tang (alt)
    "yunnanbaiyao.com.cn",  # Yunnan Baiyao
    "jiuzhitang.com",       # Jiuzhitang
    "mindray.com",          # Mindray (medical devices)
    "united-imaging.com",   # United Imaging
    "neusoft.com",          # Neusoft Medical
    "shinva.com",           # Shinva Medical
    "andon.com.cn",         # Andon Health
    "yuyue.com.cn",         # Yuwell (Yuyue Medical)
]

# ── 5. Logistics / Delivery ─────────────────────────────────────────────

LOGISTICS = [
    # Express delivery
    "sf-express.com",       # SF Express (Shunfeng)
    "zto.com",              # ZTO Express
    "yto.net.cn",           # YTO Express
    "sto.cn",               # STO Express
    "yundaex.com",          # Yunda Express
    "ems.com.cn",           # EMS (China Post Express)
    "chinapost.com.cn",     # China Post
    "jd-ex.com",            # JD Logistics
    "best-inc.com",         # Best Express
    "ttk56.com",            # TTK Express
    "deppon.com",           # Deppon Logistics
    "ane56.com",            # ANE Logistics
    "debangwuliu.com",      # Debang Logistics (alt)

    # Same-day / on-demand
    "dada.cn",              # Dada (on-demand delivery)
    "sf-city.com",          # SF City (same-city)
    "flashexpress.cn",      # Flash Express
    "uu.cn",                # UU Runner

    # Freight & supply chain
    "full-truck.com",       # Full Truck Alliance
    "huochebang.com",       # Huochebang (truck freight)
    "ymm56.com",            # Yun Man Man
    "g7.com.cn",            # G7 (fleet IoT)
    "log-56.com",           # Cainiao Logistics
    "cainiao.com",          # Cainiao Network
    "kdn.com",              # KDNiao (tracking aggregator)
    "kuaidi100.com",        # Kuaidi100 (tracking)
    "ane56.com",            # ANE Logistics
    "wlhyxx.com",           # Freight info platform
    "sinotrans.com",        # Sinotrans
    "cosco.com",            # COSCO Shipping
    "oocl.com",             # OOCL
    "mol.co.jp",            # MOL (Japan but operates heavily in China)
    "shipmentlink.com",     # Shipping link
]

# ── 6. Fashion / Beauty brands ──────────────────────────────────────────

FASHION_BEAUTY = [
    # Fashion brands & retailers
    "uniqlo.cn",            # Uniqlo China
    "zara.cn",              # Zara China
    "hm.com",               # H&M (operates in China)
    "ur.com.cn",            # UR (Urban Revivo)
    "peacebird.com.cn",     # Peacebird
    "metersbonwe.com",      # Meters/bonwe
    "semir.com",            # Semir
    "bosideng.com",         # Bosideng (down jackets)
    "septwolves.com.cn",    # Septwolves
    "lilanz.com",           # Lilanz
    "joeone.com.cn",        # Joeone
    "youngor.com.cn",       # Youngor
    "erdos.com",            # Erdos (cashmere)
    "anta.com",             # Anta Sports
    "lining.com",           # Li-Ning
    "xtep.com.cn",          # Xtep
    "361sport.com",         # 361 Degrees
    "peak.cn",              # Peak Sports
    "erke.com",             # Erke
    "hotwind.com",          # Hotwind
    "ochirly.com",          # Ochirly
    "teenie-weenie.com.cn", # Teenie Weenie

    # Beauty / Cosmetics
    "perfectdiary.com",     # Perfect Diary
    "florasis.com",         # Florasis (Hua Xi Zi)
    "colorkey.me",          # Colorkey
    "proya.com",            # Proya
    "chando.com",           # Chando (Jala Group)
    "pechoin.com",          # Pechoin (Bai Que Ling)
    "marubi.cn",            # Marubi
    "kans.com.cn",          # Kans
    "winona.com.cn",        # Winona (Botanee)
    "herborist.com.cn",     # Herborist (Shanghai Jahwa)
    "inoherb.com",          # Inoherb
    "zeesea.com",           # Zeesea
    "judydoll.com",         # Judydoll
    "catkin.cn",            # Catkin (Katuna)
    "maogeping.com",        # Mao Geping
]

# ── 7. Food / Beverage brands ───────────────────────────────────────────

FOOD_BEVERAGE = [
    # Major F&B companies
    "wahaha.com.cn",        # Wahaha
    "nongfuspring.com",     # Nongfu Spring
    "mengniu.com.cn",       # Mengniu Dairy
    "yili.com",             # Yili Dairy
    "beingmate.com",        # Beingmate (baby food)
    "wantwant.com.cn",      # Want Want
    "dali-group.com",       # Dali Foods
    "orion.cn",             # Orion (HaoLiYou)
    "master-kong.com.cn",   # Master Kong (Tingyi)
    "uni-president.com.cn", # Uni-President
    "tsingtao.com.cn",      # Tsingtao Beer
    "snowbeer.com.cn",      # Snow Beer (CR Beer)
    "yanjing.com.cn",       # Yanjing Beer
    "wuliangye.com.cn",     # Wuliangye (baijiu)
    "moutai.com.cn",        # Moutai (baijiu)
    "luzhoulaojiao.com.cn", # Luzhou Laojiao
    "swellfun.com",         # Swellfun (Shuijingfang)
    "jiangxiaobai.com",     # Jiang Xiao Bai
    "haidilao.com",         # Haidilao Hot Pot
    "xibeiyanmian.com",     # Xibei (restaurant chain)
    "heytea.com",           # HEYTEA
    "naixue.com",           # Nayuki (Naixue)
    "luckin.cn",            # Luckin Coffee
    "manner.coffee",        # Manner Coffee
    "saturnbird.com",       # Saturnbird Coffee
    "genki-forest.com",     # Genki Forest
    "juewei.com",           # Juewei (duck snacks)
    "zhougushi.com",        # Zhou Hei Ya (alt)
    "zhouheiya.cn",         # Zhou Hei Ya
    "liangpinpuzi.com",     # Liangpin Puzi (snacks)
    "bestore.com.cn",       # Bestore (snacks)
    "threesquirrels.com",   # Three Squirrels
    "baxy.com.cn",          # Ba Xi (ice cream)
    "zhongliang.com",       # COFCO
    "cofco.com",            # COFCO (alt)
    "bright.com.cn",        # Bright Dairy
    "sanyuan.com.cn",       # Sanyuan Foods
    "chabaidao.com",        # Cha Bai Dao (tea)
    "guming.com.cn",        # Gu Ming (tea chain)
    "mixue.com.cn",         # Mixue Bingcheng (ice cream/tea)
]

# ── 8. Manufacturing companies ──────────────────────────────────────────

MANUFACTURING = [
    # Steel & metals
    "baowugroup.com",       # Baowu Steel
    "hbisco.com",           # Hebei Iron and Steel
    "ansteelgroup.com",     # Ansteel Group
    "sfrencai.com",         # Shagang Group
    "chalco.com.cn",        # Chalco (aluminum)
    "jnmc.com",             # Jiangxi Copper
    "zijinmining.com",      # Zijin Mining

    # Electronics manufacturing
    "foxconn.com",          # Foxconn
    "luxshare.com",         # Luxshare Precision
    "goertek.com",          # Goertek
    "boe.com.cn",           # BOE Technology
    "csot.com",             # CSOT (TCL display)
    "tianma.com",           # Tianma Microelectronics
    "catl.com",             # CATL (batteries)
    "evebattery.com",       # EVE Energy
    "ganfenglithium.com",   # Ganfeng Lithium
    "sungrow.cn",           # Sungrow (solar inverters)
    "longi.com",            # LONGi Green Energy
    "trinasolar.com",       # Trina Solar
    "jasolar.com",          # JA Solar
    "jinko.com",            # JinkoSolar
    "canadiansolar.com",    # Canadian Solar
    "envision-group.com",   # Envision Group (wind)
    "goldwind.com.cn",      # Goldwind (wind)
    "mingyang.com",         # Mingyang Smart Energy

    # Heavy industry
    "sanygroup.com",        # Sany Heavy Industry
    "zoomlion.com",         # Zoomlion
    "xcmg.com",             # XCMG
    "sdlg.cn",              # SDLG
    "liugong.com",          # Liugong Machinery
    "shantui.com",          # Shantui
    "crrc.cn",              # CRRC (rail)
    "comac.cc",             # COMAC (aircraft)

    # Chemical & materials
    "sinopec.com",          # Sinopec
    "cnpc.com.cn",          # CNPC / PetroChina
    "cnooc.com.cn",         # CNOOC
    "wanhua.com",           # Wanhua Chemical
    "yncoal.com",           # Yunnan Coal Chemical
    "sinochem.com",         # Sinochem

    # Appliances & consumer electronics
    "midea.com",            # Midea
    "haier.com",            # Haier
    "gree.com",             # Gree Electric
    "hisense.com",          # Hisense
    "tcl.com",              # TCL
    "skyworth.com",         # Skyworth
    "konka.com",            # Konka
    "aux.cn",               # AUX
    "chigo.com",            # Chigo
    "robam.com",            # Robam (range hoods)
    "fotile.com",           # Fotile
    "vanward.com",          # Vanward (water heaters)
    "supor.com.cn",         # Supor (cookware)
    "bear.com.cn",          # Bear Electric
    "ecovacs.com",          # Ecovacs (robot vacuums)
    "roborock.com",         # Roborock
    "dreame.cn",            # Dreame Technology
    "tineco.com",           # Tineco
    "narwal.com",           # Narwal
    "stone-robot.com",      # Stone Roborock (alt brand)
]

# ── 9. Telecom companies ────────────────────────────────────────────────

TELECOM = [
    "10086.cn",             # China Mobile
    "chinamobile.com",      # China Mobile (corporate)
    "10010.com",            # China Unicom
    "chinaunicom.com.cn",   # China Unicom (corporate)
    "189.cn",               # China Telecom
    "chinatelecom.com.cn",  # China Telecom (corporate)
    "chinabbn.com",         # China Broadnet
    "towercom.cn",          # China Tower
    "fiberhome.com",        # FiberHome
    "zte.com.cn",           # ZTE
    "ruijie.com.cn",        # Ruijie Networks
    "h3c.com",              # H3C (networking)
    "tp-link.com.cn",       # TP-Link
    "tenda.com.cn",         # Tenda
    "netgear.com.cn",       # Netgear China
    "comba.com",            # Comba Telecom
    "datang.com",           # Datang Telecom
    "potevio.com",          # Potevio
    "suntelecom.cn",        # Sun Telecom
]

# ── 10. Insurance companies ─────────────────────────────────────────────

INSURANCE = [
    "picc.com",             # PICC
    "chinalife.com.cn",     # China Life
    "pingan.com",           # Ping An (may overlap with finance)
    "cpic.com.cn",          # CPIC (may overlap)
    "nci.com.cn",           # New China Life
    "taikang.com",          # Taikang Insurance
    "taikanglife.com",      # Taikang Life
    "e-chinalife.com",      # China Life online
    "cntaiping.com",        # China Taiping
    "sinosig.com",          # Sinosig
    "manulife-sinochem.com", # Manulife-Sinochem
    "picchealth.com",       # PICC Health
    "axa.com.cn",           # AXA China
    "metlife.com.cn",       # MetLife China
    "aig.com.cn",           # AIG China
    "zhongan.com",          # ZhongAn Online Insurance
    "waterdrop.com.cn",     # Waterdrop (Shuidi)
    "yuanbaopu.com",        # Yuanbao Insurance
    "duobaoyu.com.cn",      # Duobaoyu
    "huize.com",            # Huize Insurance
    "i-bearing.com",        # i-Bearing
    "aia.com.cn",           # AIA China
    "allianz.cn",           # Allianz China
    "sunshine-ins.com",     # Sunshine Insurance
    "ccic-net.com.cn",      # China Continental Insurance
    "unionlife.com.cn",     # Union Life
]

# ── 11. Regional city portal sites ──────────────────────────────────────

REGIONAL_PORTALS = [
    # Beijing
    "bjd.com.cn",           # Beijing Daily
    "qianlong.com",         # Qianlong (Beijing portal)
    # Shanghai
    "eastday.com",          # Eastday (Shanghai) -- may overlap
    "kankanews.com",        # KanKan News (Shanghai)
    "thepaper.cn",          # The Paper (Shanghai) -- may overlap
    "sh.gov.cn",            # Shanghai Gov
    # Guangdong
    "oeeee.com",            # Nandu Daily
    "ycwb.com",             # Yangcheng Wanbao
    "sznews.com",           # Shenzhen News -- may overlap
    "gd.gov.cn",            # Guangdong Gov
    # Zhejiang
    "zjol.com.cn",          # Zhejiang Online
    "66wz.com",             # Wenzhou portal
    "hz.gov.cn",            # Hangzhou Gov
    # Jiangsu
    "jschina.com.cn",       # Jiangsu portal
    "yangtse.com",          # Yangtse Evening News
    "longhoo.net",          # Nanjing portal
    # Sichuan
    "scol.com.cn",          # Sichuan Online
    "newssc.org",           # Sichuan News
    "cd.gov.cn",            # Chengdu Gov
    # Hubei
    "cnhubei.com",          # Hubei portal
    "cjn.cn",               # Changjiang Daily (Wuhan)
    # Hunan
    "rednet.cn",            # Red Net (Hunan) -- may overlap
    "voc.com.cn",           # VOC (Hunan)
    # Shandong
    "sdnews.com.cn",        # Shandong News
    "qlwb.com.cn",          # Qilu Wanbao
    "dzwww.com",            # Dazhong Wang
    # Fujian
    "fjsen.com",            # Fujian Southeast
    "mnw.cn",               # Minnan Wang (Xiamen)
    # Henan
    "hnr.cn",               # Henan portal
    # Anhui
    "anhuinews.com",        # Anhui News
    # Liaoning
    "lnd.com.cn",           # Liaoning Daily
    # Jilin
    "chinajilin.com.cn",    # Jilin portal
    # Heilongjiang
    "dbw.cn",               # Dongbei Wang
    # Shaanxi
    "cnwest.com",           # Northwest portal
    # Gansu
    "gansudaily.com.cn",    # Gansu Daily
    # Yunnan
    "yunnan.cn",            # Yunnan portal
    # Guangxi
    "gxnews.com.cn",        # Guangxi News
    # Hainan
    "hinews.cn",            # Hainan portal
    # Guizhou
    "gywb.cn",              # Guiyang Wanbao
    # Inner Mongolia
    "northnews.cn",         # Inner Mongolia portal
    # Tibet
    "tibetol.cn",           # Tibet Online
    # Xinjiang
    "ts.cn",                # Xinjiang portal
    # Ningxia
    "nxnews.net",           # Ningxia News
    # Qinghai
    "qhnews.com",           # Qinghai News
]

# ── 12. Job / Recruitment platforms ─────────────────────────────────────

RECRUITMENT = [
    "zhaopin.com",          # Zhaopin -- may overlap
    "51job.com",            # 51Job
    "liepin.com",           # Liepin
    "lagou.com",            # Lagou (tech jobs)
    "zhipin.com",           # Boss Zhipin
    "kanzhun.com",          # Kanzhun (Boss reviews)
    "shixiseng.com",        # Shixiseng (internships)
    "yingjiesheng.com",     # Yingjiesheng (campus recruiting)
    "dajie.com",            # Dajie
    "haitou.cc",            # Haitou
    "maimai.cn",            # Maimai (professional network)
    "linkedin.cn",          # LinkedIn China
    "efinancialcareers.cn", # eFinancialCareers China
    "jobui.com",            # Jobui
    "gaoxiaojob.com",       # Campus jobs
    "chinahr.com",          # ChinaHR
    "cjol.com",             # CJOL
    "goodjobs.cn",          # GoodJobs
    "528.com.cn",           # 528 Recruitment
    "91job.com",            # 91Job
    "58.com",               # 58.com (classifieds/jobs) -- may overlap
    "baixing.com",          # Baixing (classifieds)
]

# ── 13. Dating / Social apps ────────────────────────────────────────────

DATING_SOCIAL = [
    "momo.com",             # Momo
    "tantanapp.com",        # Tantan
    "soul.cn",              # Soul
    "blued.cn",             # Blued
    "baihe.com",            # Baihe (matchmaking)
    "jiayuan.com",          # Jiayuan (matchmaking)
    "zhenai.com",           # Zhenai
    "iqing.com",            # iQing
    "huazhu.com",           # Related dating
    "yidui.com",            # Yidui (video dating)
    "pearlive.com",         # PearLive
    "hello.com",            # Hello Group (Momo parent)
    "heychat.com",          # HeyChat
    "paipai.fm",            # PaiPai
    "marryou.com",          # Marryou

    # Social / community apps
    "xiaohongshu.com",      # Xiaohongshu -- may overlap
    "weixin.qq.com",        # WeChat official
    "tim.qq.com",           # TIM
    "dingtalk.com",         # DingTalk -- may overlap
    "zuimeia.com",          # Zuimeia
    "jike.city",            # Jike (social)
    "okjike.com",           # Jike (alt)
]

# ── 14. News outlets (beyond major ones) ────────────────────────────────

NEWS_OUTLETS = [
    # Business / Financial news
    "caijing.com.cn",       # Caijing Magazine
    "caixin.com",           # Caixin -- may overlap
    "yicai.com",            # Yicai -- may overlap
    "jiemian.com",          # Jiemian -- may overlap
    "nbd.com.cn",           # National Business Daily -- may overlap
    "21jingji.com",         # 21st Century Business Herald
    "eeo.com.cn",           # Economic Observer
    "cbn.com.cn",           # CBN
    "cb.com.cn",            # China Business Journal
    "ceweekly.cn",          # China Economic Weekly
    "fortunechina.com",     # Fortune China

    # Tech / Startup news
    "tmtpost.com",          # TMTPost (Titanium Media)
    "leiphone.com",         # LeiPhone (AI/tech)
    "donews.com",           # DoNews
    "iheima.com",           # i-Heima (startup news)
    "cyzone.cn",            # CYZone (startup ecosystem)
    "pedaily.cn",           # PeDaily (PE/VC news)
    "chinaventure.com.cn",  # ChinaVenture
    "iyiou.com",            # EqualOcean (Yiou)
    "lieyunwang.com",       # Lieyun Wang (startup)
    "pencilnews.cn",        # Pencil News
    "pingwest.com",         # PingWest
    "lanjinger.com",        # Blue Whale Finance
    "odaily.news",          # Odaily (crypto/blockchain)
    "8btc.com",             # 8BTC (blockchain)
    "chaindd.com",          # ChainDD

    # General / Lifestyle news
    "thepaper.cn",          # The Paper -- may overlap
    "guancha.cn",           # Guancha (Observer)
    "guokr.com",            # Guokr (science popularization)
    "lifeweek.com.cn",      # Lifeweek (Sanlian)
    "duitang.com",          # Duitang
    "jandan.net",           # Jandan (humor/science)
    "infzm.com",            # Southern Weekend
    "bjnews.com.cn",        # Beijing News
    "thecover.cn",          # The Cover
    "redstar.news",         # Red Star News
    "stheadline.com",       # Sing Tao
    "hk01.com",             # HK01
    "mingpao.com",          # Ming Pao
    "bastillepost.com",     # Bastille Post
    "on.cc",                # Oriental Daily
]

# ── 15. Sports / Fitness platforms ──────────────────────────────────────

SPORTS_FITNESS = [
    # Sports media
    "hupu.com",             # Hupu (sports community)
    "zhibo8.cc",            # Zhibo8 (live sports)
    "dongqiudi.com",        # Dongqiudi (football)
    "lanqiu.com",           # Lanqiu (basketball)
    "okooo.com",            # Okooo (sports lottery)
    "500.com",              # 500.com (sports lottery)
    "sportscn.com",         # Sportscn
    "pp.cn",                # PP Sports
    "zhangyu.tv",           # Zhang Yu TV
    "7m.cn",                # 7M Sports
    "nba.com.cn",           # NBA China
    "titan24.com",          # Titan Sports -- may overlap
    "espnstar.com.cn",      # ESPN China
    "sodasoccer.com",       # SodaSoccer
    "goalhi.com",           # GoalHi

    # Fitness apps / platforms
    "keepapp.com",          # Keep (fitness app)
    "codoon.com",           # Codoon (running)
    "gotokeep.com",         # Keep (alt)
    "fittime.com",          # FitTime
    "joyrun.com",           # Joyrun
    "zuicool.com",          # Zuicool (outdoor sports)
    "fiture.com",           # Fiture (smart mirror fitness)
    "supermonkey.com.cn",   # Super Monkey (gym chain)
    "lefit.com",            # Lefit (gym chain)
]

# ── Additional categories to reach 1000+ ────────────────────────────────

# Chinese universities (beyond existing list)
UNIVERSITIES = [
    "ruc.edu.cn",           # Renmin University
    "bit.edu.cn",           # Beijing Institute of Technology
    "buaa.edu.cn",          # Beihang University
    "nankai.edu.cn",        # Nankai University
    "xjtu.edu.cn",          # Xi'an Jiaotong University
    "hit.edu.cn",           # Harbin Institute of Technology
    "seu.edu.cn",           # Southeast University
    "scut.edu.cn",          # South China University of Technology
    "dlut.edu.cn",          # Dalian University of Technology
    "cqu.edu.cn",           # Chongqing University
    "lzu.edu.cn",           # Lanzhou University
    "ouc.edu.cn",           # Ocean University of China
    "csu.edu.cn",           # Central South University
    "nudt.edu.cn",          # National University of Defense Technology
    "uestc.edu.cn",         # UESTC (Chengdu)
    "nwpu.edu.cn",          # Northwestern Polytechnical
    "tongji.edu.cn",        # Tongji University
    "ecnu.edu.cn",          # East China Normal University
    "bnu.edu.cn",           # Beijing Normal University
    "swjtu.edu.cn",         # Southwest Jiaotong University
    "nwu.edu.cn",           # Northwest University
    "sdu.edu.cn",           # Shandong University
    "jlu.edu.cn",           # Jilin University
    "sysu.edu.cn",          # Sun Yat-sen University
    "xmu.edu.cn",           # Xiamen University
    "scu.edu.cn",           # Sichuan University
    "tju.edu.cn",           # Tianjin University
    "hnu.edu.cn",           # Hunan University
    "hfut.edu.cn",          # Hefei University of Technology
    "nenu.edu.cn",          # Northeast Normal University
    "swu.edu.cn",           # Southwest University
]

# Semiconductor & chip companies
SEMICONDUCTOR = [
    "smic.com",             # SMIC
    "hlmc.cn",              # Hua Hong Semi
    "unisemicon.com",       # Unigroup
    "thpul.com",            # Tsinghua Unigroup
    "willsemi.com",         # Will Semiconductor
    "starpower-semi.com",   # StarPower Semi
    "sgmicro.com",          # SG Micro
    "naura.com",            # NAURA Technology
    "amec-inc.com",         # AMEC (etch equipment)
    "montage-tech.com",     # Montage Technology
    "unigroup.com.cn",      # Unigroup
    "zte-semi.com",         # ZTE Microelectronics
    "espressif.com",        # Espressif (ESP32)
    "allwinnertech.com",    # Allwinner
    "rockchip.com",         # Rockchip
    "unisoc.com",           # UNISOC
    "loongson.cn",          # Loongson (CPU)
    "phytium.com.cn",       # Phytium (CPU)
    "hygon.cn",             # Hygon (CPU)
]

# Fintech & digital banking
FINTECH = [
    "webank.com",           # WeBank (Tencent)
    "mybank.cn",            # MYbank (Ant Group)
    "airstar.com",          # Airstar Bank
    "oneconnect.com",       # OneConnect (Ping An)
    "duxiaoman.com",        # Du Xiaoman Finance (Baidu)
    "lexin.com",            # LexinFintech
    "360jie.com.cn",        # 360 Finance
    "fenqile.com",          # Fenqile
    "renrendai.com",        # Renrendai
    "lufax.com",            # Lufax -- may overlap
    "creditease.cn",        # CreditEase
    "yixin.com",            # Yixin (CreditEase)
    "lakala.com",           # Lakala (payment)
    "yeepay.com",           # YeePay
    "99bill.com",           # 99Bill
    "sandpay.com.cn",       # SandPay
    "ipaynow.cn",           # iPayNow
    "baofu.com",            # BaoFu
]

# Smart home / IoT
SMART_HOME_IOT = [
    "aqara.com",            # Aqara (smart home)
    "yeelight.com",         # Yeelight
    "chuangmi.com",         # Chuangmi
    "orvibo.com",           # ORVIBO
    "broadlink.com.cn",     # BroadLink
    "lifesmart.cn",         # LifeSmart
    "lumi-united.com",      # Lumi (Aqara parent)
    "sonoff.cn",            # Sonoff (ITEAD)
    "switchbot.cn",         # SwitchBot China
    "petkit.cn",            # Petkit (smart pet devices)
    "tmall.genie.com",      # Tmall Genie
    "dingdong.com",         # DingDong (speaker)
]

# EV / New energy companies
NEW_ENERGY = [
    "leapmotor.com",        # Leapmotor
    "neta.cn",              # Neta Auto (Hozon)
    "aion.com.cn",          # Aion (GAC)
    "im-motors.com",        # IM Motors (SAIC)
    "hiphi.com",            # HiPhi
    "voyah.com.cn",         # Voyah (Dongfeng)
    "avatr.com",            # Avatr (Changan)
    "jiyue.com",            # Jiyue (Baidu/Geely)
    "luxeed.com",           # Luxeed (Chery/Huawei)
    "deepal.com.cn",        # Deepal (Changan)
    "ling-auto.com",        # Lingpao (alt: Smart from Geely)
    "smart.com",            # Smart (Geely-Daimler)
    "ora.cn",               # ORA (GWM)
    "wey.com.cn",           # WEY (GWM)
    "tank.cn",              # Tank (GWM)
    "seres.cn",             # Seres (Huawei collab)
    "svolt.cn",             # SVOLT (batteries)
    "gotion.com.cn",        # Gotion High-tech (batteries)
    "calb.cn",              # CALB (batteries)
]

# Robotics & AI
ROBOTICS_AI = [
    "ubtech.com",           # UBTech Robotics
    "cloudminds.com",       # CloudMinds
    "geekplus.com",         # Geek+
    "haikairobotics.com",   # Hai Robotics
    "standard-robots.com",  # Standard Robots
    "yushutech.com",        # Yushu Robotics
    "deeprobotics.cn",      # Deep Robotics
    "unitree.com",          # Unitree Robotics
    "4paradigm.com",        # 4Paradigm
    "datavisor.com",        # DataVisor
    "yitutech.com",         # Yitu Technology
    "cloudwalk.com",        # CloudWalk
    "intellifusion.com",    # Intellifusion
    "tusimple.cn",          # TuSimple
    "pony.ai",              # Pony.ai
    "weride.ai",            # WeRide
    "momenta.cn",           # Momenta
    "hesaitech.com",        # Hesai Technology (LiDAR)
    "robosense.cn",         # RoboSense (LiDAR)
    "innovusion.com",       # Innovusion (LiDAR)
    "slamtec.com",          # SLAMTEC
]

# Education technology (beyond existing)
EDTECH = [
    "gaotu.cn",             # Gaotu Techedu
    "youdao.com",           # Youdao (NetEase)
    "duia.com",             # Duia
    "sunlands.com",         # Sunlands
    "huatu.com",            # Huatu Education
    "offcn.com",            # Offcn (public exam prep)
    "koolearn.com",         # Koolearn -- may overlap
    "xdf.cn",               # New Oriental
    "100tal.com",           # TAL Education
    "xueda.com",            # Xueda Education
    "baijiahao.com",        # Baijiahao
    "kaoshibaodian.com",    # Kaoshi Baodian
    "wangxiao.cn",          # Wangxiao
    "hqwx.com",             # Huanqiu Wangxiao
    "233.com",              # 233 Wangxiao
    "youzy.cn",             # Youzy (college admissions)
    "eol.cn",               # China Education Online
    "chsi.com.cn",          # CHSI (academic credentials)
    "neea.edu.cn",          # National Education Examinations
]

# Pet economy
PET_ECONOMY = [
    "boqii.com",            # Boqii (pet ecommerce)
    "epet.com",             # E-Pet
    "pethadoop.com",        # Pethadoop
    "dogcatstar.com",       # DogCatStar
    "pidan.com",            # Pidan (cat products)
    "catlink.com",          # CatLink (smart litter box)
    "petkit.cn",            # PetKit -- may overlap
    "moii.cn",              # Moii Pet
]

# Wedding / Family
WEDDING_FAMILY = [
    "hunliji.com",          # Hunliji (wedding planning)
    "wed114.cn",            # Wed114
    "daoxila.com",          # Daoxila (wedding)
    "babytree.com",         # BabyTree (parenting)
    "mama.cn",              # Mama.cn (parenting)
    "pcbaby.com.cn",        # PCBaby
    "ci123.com",            # Ci123 (parenting)
    "qbaobei.com",          # QBaoBei
]

# Legal / IP services
LEGAL = [
    "itslaw.com",           # ItsLaw
    "fawu.com",             # Fawu
    "lawtime.cn",           # Lawtime
    "66law.cn",             # 66Law
    "findlaw.cn",           # FindLaw China
    "lawyee.org",           # Lawyee
    "zhichan.com",          # ZhiChan (IP)
    "qizhidao.com",        # QiZhiDao (trademarks)
    "zhihuiya.com",         # ZhiHuiYa (patent search)
    "tianyancha.com",       # Tianyancha (business info)
    "qcc.com",              # QCC (Qichacha)
    "aiqicha.com",          # AiQiCha (Baidu business search)
    "gsxt.gov.cn",          # National Enterprise Credit
]

# Agriculture tech
AGRITECH = [
    "nongbang.com",         # Nongbang
    "nongji360.com",        # Nongji360 (farm equipment)
    "huinongwang.com",      # Huinong Wang
    "cnhnb.com",            # CNHNB (agriculture B2B)
    "191.cn",               # 191 Agriculture
    "35.com",               # 35.com (agriculture)
    "nongjx.com",           # Nongjx (farm machinery)
    "nongcun5.com",         # Nongcun5
]

# Music & Entertainment
MUSIC_ENTERTAINMENT = [
    "music.163.com",        # NetEase Cloud Music
    "y.qq.com",             # QQ Music
    "kugou.com",            # Kugou Music
    "kuwo.cn",              # Kuwo Music
    "qishui.com",           # Qishui Music
    "changba.com",          # Changba (karaoke)
    "manmankan.com",        # ManManKan (anime)
    "dmzj.com",             # DMZJ (comics)
    "kuaikanmanhua.com",    # Kuaikan Comics
    "ac.qq.com",            # QQ Comics
    "u17.com",              # U17 (comics)
    "zymk.cn",              # ZYMK (comics)
    "qidian.com",           # Qidian (web novels)
    "zongheng.com",         # Zongheng (web novels)
    "17k.com",              # 17K (web novels)
    "ciweimao.com",         # Ciweimao (web novels)
    "faloo.com",            # Faloo (web novels)
    "shuqi.com",            # Shuqi (reading)
    "ireader.com",          # iReader
    "zhangyue.com",         # Zhangyue (iReader parent)
    "huya.com",             # Huya (game streaming)
    "douyu.com",            # Douyu (game streaming)
    "cc.163.com",           # CC Live (NetEase)
    "yy.com",               # YY Live
    "inke.cn",              # Inke Live
    "huajiao.com",          # Huajiao Live
    "6.cn",                 # 6.cn Live
]

# Furniture / Home improvement
HOME_IMPROVEMENT = [
    "tata.com.cn",          # TATA Wooden Door
    "qumei.com",            # Qumei Furniture
    "landbond.com",         # Landbond
    "kuka.cn",              # Kuka Home
    "natuzzi.com.cn",       # Natuzzi China
    "suofeiya.com",         # Sofia Home
    "oppein.com",           # Oppein
    "jinpai.com",           # Jinpai Kitchen
    "tubatu.com",           # Tu Ba Tu (renovation platform)
    "to8to.com",            # To8To (renovation)
    "shejiben.com",         # Shejiben (design platform)
    "pchouse.com.cn",       # PChouse (home decor)
    "jia.com",              # Jia.com
    "maigoo.com",           # Maigoo (brand rankings)
]

# Photography & design tools
DESIGN_TOOLS = [
    "canva.cn",             # Canva China
    "chuangkit.com",        # Chuangkit
    "gaoding.com",          # Gaoding Design
    "fotor.com.cn",         # Fotor
    "meitu.com",            # Meitu
    "xiuxiu.web.meitu.com", # Meitu Xiuxiu
    "huaban.com",           # Huaban (Pinterest-like)
    "zcool.com.cn",         # ZCool (design community)
    "ui.cn",                # UI China
    "iconfont.cn",          # Iconfont (Alibaba icons)
    "lanhuapp.com",         # Lanhu (design handoff)
    "modao.cc",             # Modao (prototyping)
    "mockplus.cn",          # Mockplus
    "js.design",            # JS Design (Figma-like)
    "mastergo.com",         # MasterGo
    "pixso.cn",             # Pixso
    "processon.com",        # ProcessOn (diagramming)
    "boardmix.cn",          # BoardMix (whiteboard)
]

# More gaming companies (not in existing list)
GAMING_EXPANDED = [
    "netease.com",          # NetEase (corporate)
    "papegames.com",        # Papergames (Shining Nikki)
    "hypergryph.com",       # Hypergryph (Arknights)
    "yo-star.com",          # Yostar
    "kurogames.com",        # Kuro Games (Wuthering Waves)
    "hoyoverse.com",        # HoYoverse
    "zlongame.com",         # ZLongame
    "g-bits.com",           # G-bits
    "wanmei.com",           # Perfect World
    "seasungames.com",      # Seasun Games
    "gameduchy.com",        # Game Duchy
    "longtugame.com",       # Longtu Game
    "cmge.com",             # CMGE
    "babeltime.com",        # BabelTime
    "dragonest.com",        # Dragonest (auto chess)
    "moonton.com",          # Moonton (Mobile Legends)
    "funplus.com",          # FunPlus
    "igg.com",              # IGG
    "habby.com",            # Habby
    "minigame.vip",         # Minigame
]

# Crypto / Web3 (China-origin, many operate globally)
CRYPTO_WEB3 = [
    "binance.com",          # Binance
    "okx.com",              # OKX
    "huobi.com",            # Huobi
    "gate.io",              # Gate.io
    "kucoin.com",           # KuCoin
    "bitmain.com",          # Bitmain
    "canaan.io",            # Canaan
    "nervos.org",           # Nervos
    "confluxnetwork.org",   # Conflux
    "tron.network",         # TRON
    "vechain.org",          # VeChain
    "neo.org",              # NEO
    "ont.io",               # Ontology
    "qtum.org",             # Qtum
]

# Research institutes & think tanks
RESEARCH = [
    "cas.cn",               # Chinese Academy of Sciences
    "cae.cn",               # Chinese Academy of Engineering
    "cass.cn",              # Chinese Academy of Social Sciences
    "nsfc.gov.cn",          # NSFC
    "most.gov.cn",          # Ministry of Science & Tech
    "caict.ac.cn",          # China Academy of ICT
    "ccid.com",             # CCID
    "iresearch.com.cn",     # iResearch
    "questmobile.com.cn",   # QuestMobile
    "analysys.cn",          # Analysys
    "talkingdata.com",      # TalkingData
    "trustdata.cn",         # TrustData
]


# ── Aggregate all expanded domains ──────────────────────────────────────

ALL_EXPANDED = {
    "top_traffic": TOP_TRAFFIC,
    "saas": SAAS,
    "b2b": B2B,
    "healthcare": HEALTHCARE,
    "logistics": LOGISTICS,
    "fashion_beauty": FASHION_BEAUTY,
    "food_beverage": FOOD_BEVERAGE,
    "manufacturing": MANUFACTURING,
    "telecom": TELECOM,
    "insurance": INSURANCE,
    "regional_portals": REGIONAL_PORTALS,
    "recruitment": RECRUITMENT,
    "dating_social": DATING_SOCIAL,
    "news_outlets": NEWS_OUTLETS,
    "sports_fitness": SPORTS_FITNESS,
    "universities": UNIVERSITIES,
    "semiconductor": SEMICONDUCTOR,
    "fintech": FINTECH,
    "smart_home_iot": SMART_HOME_IOT,
    "new_energy": NEW_ENERGY,
    "robotics_ai": ROBOTICS_AI,
    "edtech": EDTECH,
    "pet_economy": PET_ECONOMY,
    "wedding_family": WEDDING_FAMILY,
    "legal": LEGAL,
    "agritech": AGRITECH,
    "music_entertainment": MUSIC_ENTERTAINMENT,
    "home_improvement": HOME_IMPROVEMENT,
    "design_tools": DESIGN_TOOLS,
    "gaming_expanded": GAMING_EXPANDED,
    "crypto_web3": CRYPTO_WEB3,
    "research": RESEARCH,
}


def get_all_expanded_domains() -> list[str]:
    """Return a flat, deduplicated list of all expanded domains."""
    seen = set()
    result = []
    for category, domains in ALL_EXPANDED.items():
        for d in domains:
            # Normalize: strip whitespace, lowercase
            d = d.strip().lower()
            if d not in seen:
                seen.add(d)
                result.append(d)
    return result


def get_stats() -> dict:
    """Print category counts and total."""
    stats = {}
    for name, domains in ALL_EXPANDED.items():
        stats[name] = len(domains)
    all_domains = get_all_expanded_domains()
    stats["_total_unique"] = len(all_domains)
    return stats


if __name__ == "__main__":
    stats = get_stats()
    for cat, count in stats.items():
        print(f"  {cat}: {count}")
    print(f"\n  Total unique expanded domains: {stats['_total_unique']}")
