#!/usr/bin/env python3
"""
微博热搜 API 客户端
用于抓取微博热搜榜单数据
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime


class WeiboHotSearchClient:
    """微博热搜 API 客户端"""

    # 常用的微博热搜 API 端点
    ENDPOINTS = {
        "tianapi": "https://apis.tianapi.com/weibohot/index?key=c533afd4ff38005496594b80eb6bd27c",
        "weibo_cn": "https://weibo.com/ajax/side/hotSearch",
        "rank_whatever": "https://api.rank-whatever.com/v1/weibo/hot",
        # 用户可以添加自定义端点
    }

    def __init__(self, endpoint: str = "tianapi", timeout: int = 10):
        """
        初始化客户端

        Args:
            endpoint: API 端点名称或 URL
            timeout: 请求超时时间（秒）
        """
        self.endpoint = self.ENDPOINTS.get(endpoint, endpoint)
        self.timeout = timeout
        self.session = requests.Session()
        # 设置常用的请求头
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })

    def fetch_hot_search(self) -> List[Dict[str, any]]:
        """
        抓取微博热搜榜单

        Returns:
            热搜话题列表，每个话题包含:
            - rank: 排名
            - topic: 话题标题
            - heat: 热度值
            - category: 分类
            - url: 链接
        """
        try:
            response = self.session.get(self.endpoint, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            # 解析不同 API 的响应格式
            topics = self._parse_response(data)

            return topics

        except requests.exceptions.RequestException as e:
            print(f"❌ API 请求失败: {e}")
            return []
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            return []
        except Exception as e:
            print(f"❌ 未知错误: {e}")
            return []

    def _parse_response(self, data: Dict) -> List[Dict[str, any]]:
        """
        解析 API 响应数据

        Args:
            data: API 返回的原始数据

        Returns:
            标准化的话题列表
        """
        topics = []

        # 根据不同的 API 格式进行解析
        if 'result' in data and 'list' in data['result']:
            # 天行数据 API 格式
            for idx, item in enumerate(data['result']['list'], 1):
                hotword = item.get('hotword', '').strip()
                hot_num = item.get('hotwordnum', '0').replace(',', '').replace(' ', '')
                hot_tag = item.get('hottag', '')

                try:
                    heat = int(hot_num)
                except ValueError:
                    heat = 0

                topics.append({
                    'rank': idx,
                    'topic': hotword,
                    'heat': heat,
                    'category': hot_tag if hot_tag else '热搜',
                    'url': f"https://s.weibo.com/weibo?q={hotword}"
                })

        elif 'data' in data and 'realtime' in data['data']:
            # 微博官方 API 格式
            for item in data['data']['realtime']:
                topics.append({
                    'rank': item.get('rank', 0),
                    'topic': item.get('word', ''),
                    'heat': item.get('num', 0),
                    'category': item.get('category', ''),
                    'url': f"https://s.weibo.com/weibo?q={item.get('word', '')}"
                })

        elif 'list' in data:
            # 通用列表格式
            for idx, item in enumerate(data['list'], 1):
                topics.append({
                    'rank': idx,
                    'topic': item.get('title', item.get('topic', item.get('word', ''))),
                    'heat': item.get('hot', item.get('heat', item.get('num', 0))),
                    'category': item.get('category', ''),
                    'url': item.get('url', item.get('link', ''))
                })

        else:
            print("⚠️  未知的 API 响应格式，尝试通用解析")
            # 通用解析尝试
            for idx, item in enumerate(data if isinstance(data, list) else [data], 1):
                topics.append({
                    'rank': idx,
                    'topic': str(item.get('word', item.get('title', ''))),
                    'heat': item.get('num', item.get('hot', 0)),
                    'category': '',
                    'url': ''
                })

        return topics

    def save_to_json(self, topics: List[Dict], filename: Optional[str] = None):
        """
        保存热搜数据到 JSON 文件

        Args:
            topics: 话题列表
            filename: 文件名（可选，默认使用时间戳）
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"weibo_hot_search_{timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(topics, f, ensure_ascii=False, indent=2)
            print(f"✅ 数据已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存文件失败: {e}")

    def display_topics(self, topics: List[Dict], limit: int = 20):
        """
        打印热搜话题到控制台

        Args:
            topics: 话题列表
            limit: 显示数量限制
        """
        print(f"\n{'='*60}")
        print(f"🔥 微博热搜榜单 (Top {min(limit, len(topics))})")
        print(f"{'='*60}\n")

        for topic in topics[:limit]:
            rank_emoji = "🥇" if topic['rank'] == 1 else "🥈" if topic['rank'] == 2 else "🥉" if topic['rank'] == 3 else f"#{topic['rank']:2d}"
            heat_display = self._format_heat(topic['heat'])

            print(f"{rank_emoji}  {topic['topic']}")
            print(f"      热度: {heat_display} | 分类: {topic['category'] or '未知'}")
            print()

    @staticmethod
    def _format_heat(heat: int) -> str:
        """
        格式化热度值显示

        Args:
            heat: 原始热度值

        Returns:
            格式化后的热度字符串
        """
        if heat >= 1000000:
            return f"{heat/1000000:.2f}M"
        elif heat >= 1000:
            return f"{heat/1000:.1f}K"
        else:
            return str(heat)


def main():
    """主函数 - 用于测试"""
    print("🚀 正在抓取微博热搜...\n")

    client = WeiboHotSearchClient()
    topics = client.fetch_hot_search()

    if topics:
        client.display_topics(topics, limit=20)
        client.save_to_json(topics)
        print(f"\n✅ 成功获取 {len(topics)} 条热搜话题")
    else:
        print("\n❌ 未能获取热搜数据，请检查 API 端点或网络连接")


if __name__ == "__main__":
    main()
