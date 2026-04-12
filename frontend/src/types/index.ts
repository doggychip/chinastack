export interface Detection {
  tech_id: string;
  tech_name: string;
  tech_slug: string;
  category: string;
  website?: string;
  description?: string;
  version?: string;
  confidence: number;
  evidence?: string;
}

export interface SiteResult {
  domain: string;
  url: string;
  title?: string;
  icp_number?: string;
  status_code?: number;
  response_time_ms?: number;
  tech_count: number;
  detections: Detection[];
  cached: boolean;
}

export interface SiteListItem {
  id: string;
  domain: string;
  url: string;
  title?: string;
  icp_number?: string;
  status_code?: number;
  response_time_ms?: number;
  last_scanned_at?: string;
  scan_count: number;
  tech_count: number;
}

export interface TechnologyItem {
  id: string;
  name: string;
  slug: string;
  category: string;
  subcategory?: string;
  website?: string;
  description?: string;
  site_count: number;
}

export interface CategoryStat {
  key: string;
  label: string;
  tech_count: number;
}

export interface OverviewStats {
  total_sites: number;
  total_technologies: number;
  total_detections: number;
  categories: CategoryStat[];
}

export interface TopTech {
  name: string;
  slug: string;
  category: string;
  category_label: string;
  count: number;
  percentage: number;
}

export interface CategoryDetail {
  category: string;
  category_label: string;
  technologies: {
    name: string;
    slug: string;
    count: number;
    percentage: number;
  }[];
}

export const CATEGORIES: Record<string, string> = {
  analytics: "数据分析",
  payment: "支付",
  cdn: "CDN",
  framework_fe: "前端框架",
  framework_be: "后端框架",
  cms: "CMS",
  ecommerce: "电商平台",
  cloud: "云服务",
  miniprogram: "小程序",
  advertising: "广告",
  customer_service: "客服",
  map: "地图",
  security: "安全",
  font: "字体",
  video: "视频",
  social: "社交",
  server: "服务器",
  javascript: "JS库",
  ui: "UI组件库",
  tag_manager: "标签管理",
  hosting: "托管",
  email: "邮件",
  other: "其他",
};

export const CATEGORY_COLORS: Record<string, string> = {
  analytics: "#3B82F6",
  payment: "#10B981",
  cdn: "#8B5CF6",
  framework_fe: "#F59E0B",
  framework_be: "#EF4444",
  cms: "#EC4899",
  ecommerce: "#14B8A6",
  cloud: "#6366F1",
  miniprogram: "#22C55E",
  advertising: "#F97316",
  customer_service: "#06B6D4",
  map: "#84CC16",
  security: "#DC2626",
  font: "#A855F7",
  video: "#E11D48",
  social: "#2563EB",
  server: "#64748B",
  javascript: "#EAB308",
  ui: "#D946EF",
  tag_manager: "#0EA5E9",
  hosting: "#7C3AED",
  email: "#F43F5E",
  other: "#94A3B8",
};
