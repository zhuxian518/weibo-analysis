#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微博热搜分析配置文件
集中管理 API 和其他配置
"""

# API 配置
WEIBO_HOT_API = {
    "provider": "天行数据 (TianAPI)",
    "endpoint": "https://apis.tianapi.com/weibohot/index",
    "api_key": "c533afd4ff38005496594b80eb6bd27c",
    "full_url": "https://apis.tianapi.com/weibohot/index?key=c533afd4ff38005496594b80eb6bd27c",
    "method": "GET",
    "timeout": 10,
    "response_format": "json"
}

# 分析配置
ANALYSIS_CONFIG = {
    "max_topics": 10,          # 分析的热搜话题数量
    "min_heat": 1000,          # 最小热度值（低于此值的话题会被过滤）
    "min_score": 60,           # 最小创意评分（低于此值的创意不会展示）
    "excellent_threshold": 80  # 优秀创意评分阈值
}

# 评分权重
SCORING_WEIGHTS = {
    "interestingness": 80,     # 有趣度权重
    "usefulness": 20           # 有用度权重
}

# 输出配置
OUTPUT_CONFIG = {
    "html_template": "html-template.html",
    "output_prefix": "weibo-analysis",
    "timestamp_format": "%Y%m%d_%H%M%S"
}

# Web 搜索配置
WEB_SEARCH_CONFIG = {
    "search_engine": "web-search-prime",  # 使用 web-search-prime 工具
    "location": "cn",                      # 中国地区
    "recency": "oneWeek",                 # 搜索最近一周的内容
    "max_results": 5,                      # 每个话题最多搜索次数
    "content_size": "medium"               # 内容大小
}

# 产品创意模板
PRODUCT_IDEA_TEMPLATES = {
    "gift": {
        "keywords": ["送", "礼", "品", "赠", "奖"],
        "idea_suffix": "智能礼品管理平台",
        "target_users": "25-40岁品牌营销人员"
    },
    "healthcare": {
        "keywords": ["药", "医", "疗", "康", "健"],
        "idea_suffix": "医疗健康助手",
        "target_users": "30-55岁患者及家属"
    },
    "logistics": {
        "keywords": ["港", "运", "物", "流", "配"],
        "idea_suffix": "智能物流调度",
        "target_users": "贸易公司、货运代理"
    },
    "social": {
        "keywords": ["婚", "恋", "情感", "关系"],
        "idea_suffix": "情感咨询平台",
        "target_users": "25-45岁已婚人群"
    },
    "lifestyle": {
        "keywords": ["岁", "年龄", "成长", "生活"],
        "idea_suffix": "生活交流社区",
        "target_users": "18-35岁年轻人"
    }
}
