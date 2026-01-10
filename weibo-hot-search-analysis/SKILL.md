---
name: weibo-hot-search-analysis
description: "Comprehensive Weibo hot search trending topics analyzer that fetches trending topics, performs background research via web search, analyzes product opportunities, and generates detailed HTML reports with scoring and visualization. Use when user needs to: (1) Analyze Weibo trending topics for product insights, (2) Generate creative product ideas based on social media trends, (3) Research background information on trending topics, (4) Create structured reports with product opportunity scoring and recommendations. Ideal for product managers, entrepreneurs, and market researchers seeking data-driven product inspiration from Chinese social media trends."
license: MIT
---

# Weibo Hot Search Product Idea Analysis

## Overview

This skill analyzes Weibo hot search trending topics to extract product development opportunities through automated data collection, web research, AI-powered analysis, and professional HTML reporting.

## Quick Start

When this skill is activated, follow these steps:

1. **Fetch Data**: Call Weibo hot search API: `https://apis.tianapi.com/weibohot/index?key=c533afd4ff38005496594b80eb6bd27c`
2. **Research**: Use web search tools for background on each topic
3. **Generate Ideas**: Create product concepts with 80/20 scoring framework (Interestingness 80% + Usefulness 20%)
4. **Create Report**: Generate HTML using [`html-template.html`](html-template.html)

## Implementation Steps

### Phase 1: Fetch Weibo Hot Search Data

```bash
curl "https://apis.tianapi.com/weibohot/index?key=c533afd4ff38005496594b80eb6bd27c"
```

Parse JSON response and extract trending topics (typically top 50). Filter out topics with zero heat values.

### Phase 2: Background Research

For each topic, perform web searches to gather:
- Topic context and timeline
- Key entities and stakeholders
- Public sentiment and reactions
- Related trends

**Tool**: Use `mcp__web-search-prime__webSearchPrime` or `WebSearch` with `search_recency_filter: oneWeek` and `location: cn`

### Phase 3: Product Idea Generation & Scoring

**Scoring Framework** (100 points total):

| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **Interestingness** | 80 points | Novelty, creativity, viral potential, uniqueness, entertainment value |
| **Usefulness** | 20 points | Solves real problem, market demand, feasibility, user value |

For each idea, provide:
1. **Product Name**: Creative and memorable
2. **Core Function**: 2-3 sentences describing what it does
3. **Target Users**: Detailed persona (demographics, psychographics, pain points)
4. **Composite Score**: Breakdown of interestingness/usefulness
5. **Rationale**: Why this idea scores well

**Quality Threshold**:
- Only include ideas with score ≥ 60/100
- ≥80/100: Mark as **Excellent**
- 60-79/100: Mark as **Good**

### Phase 4: Generate HTML Report

Use the template at [`html-template.html`](html-template.html) and populate with:
- Total topics analyzed
- Total ideas generated
- Excellent ideas count
- Individual topic cards with research findings and product ideas

**Output**: Save as `weibo-analysis-[timestamp].html`

## Error Handling

- **API Failure**: Log error and ask user for alternative data source
- **No Search Results**: Mark topic as "Insufficient data" and skip
- **Low Quality Ideas**: Report "No viable product ideas found"
- **HTML Template Error**: Fall back to basic HTML structure

## Success Criteria

✅ All trending topics fetched from API
✅ Background research completed for each topic
✅ At least 1 product idea per topic (when feasible)
✅ All ideas scored using 80/20 framework
✅ HTML report generated with proper formatting
✅ High-scoring ideas (≥80) prominently highlighted

## Tools Required

1. **HTTP Client**: Bash curl or Python requests for API calls
2. **Web Search**: `mcp__web-search-prime__webSearchPrime` or `WebSearch`
3. **File Operations**: `Read` and `Write` tools for report generation

## Reference Files

- [`html-template.html`](html-template.html) - Complete HTML report template with styling
- [`README.md`](README.md) - Detailed documentation and usage examples
- [`api-client.py`](api-client.py) - Python API client (optional)
- [`config.py`](config.py) - Configuration management (optional)

## Limitations

1. **API Rate Limits**: Respect API rate limits, implement delays if needed
2. **Research Depth**: Limited to publicly available web content
3. **Language**: Optimized for Chinese content
4. **Processing Time**: Full analysis of 20 topics may take 5-10 minutes
5. **Subjectivity**: Product scoring combines objective metrics with AI judgment

---

**Version**: 2.0
**Last Updated**: 2026-01-11
