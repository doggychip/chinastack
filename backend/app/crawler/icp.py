import re

ICP_PATTERNS = [
    re.compile(r'([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁]ICP备\d{6,}号(?:-\d+)?)'),
    re.compile(r'(增值电信业务经营许可证[：:]\s*[京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁]B\d-\d+)'),
    re.compile(r'([京津沪渝冀豫云辽黑湘皖鲁新苏浙赣鄂桂甘晋蒙陕吉闽贵粤川青藏琼宁]公网安备\s*\d+号)'),
]


def extract_icp(html: str) -> dict:
    """Extract ICP filing number from page HTML.
    Usually in the footer as: 京ICP备09001948号 or 粤B2-20090059
    """
    result = {}
    for pattern in ICP_PATTERNS:
        m = pattern.search(html)
        if m:
            result["icp_number"] = m.group(1)
            break
    return result
