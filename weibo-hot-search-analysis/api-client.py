#!/usr/bin/env python3
"""
微博热搜 API 客户端
用于抓取微博热搜榜单数据
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urlsplit, parse_qsl

from config import WEIBO_HOT_API, get_tianapi_key


class WeiboHotSearchClient:
    """微博热搜 API 客户端"""

    # Never put credentials in endpoint URLs or commit them to source control.
    ENDPOINTS = {
        "tianapi": WEIBO_HOT_API["endpoint"],
        "weibo_cn": "https://weibo.com/ajax/side/hotSearch",
        "rank_whatever": "https://api.rank-whatever.com/v1/weibo/hot",
    }

    def __init__(self, endpoint: str = "tianapi", timeout: int = 10,
                 api_key: Optional[str] = None):
        """Use TIANAPI_KEY for TianAPI; other HTTPS endpoints need no shared key."""
        self.endpoint = self.ENDPOINTS.get(endpoint, endpoint)
        try:
            parts = urlsplit(self.endpoint)
            secret_fields = {"key", "token", "api_key", "apikey", "access_token",
                             "authorization", "password", "secret"}
            if (parts.scheme != "https" or not parts.hostname or parts.username
                    or parts.password or parts.fragment
                    or any(key.lower() in secret_fields for key, _ in parse_qsl(parts.query, keep_blank_values=True))):
                raise ValueError
        except (ValueError, TypeError):
            raise ValueError("端点须为HTTPS且不能包含登录信息或密钥参数。") from None
        self._params = {}
        if self.endpoint == self.ENDPOINTS["tianapi"]:
            self._params["key"] = get_tianapi_key(api_key)
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
            response = self.session.get(self.endpoint, params=self._params,
                                        timeout=self.timeout, allow_redirects=False)
            if 300 <= response.status_code < 400:
                print("❌ API 返回重定向，已停止，避免将凭据转发至其他地址。")
                return []
            response.raise_for_status()
            data = response.json()

            if (self.endpoint == self.ENDPOINTS["tianapi"] and isinstance(data, dict)
                    and "code" in data and data["code"] not in (200, "200")):
                print("❌ API 返回业务错误，请在服务控制台检查密钥、权限或额度。")
                return []

            # 解析不同 API 的响应格式
            topics = self._parse_response(data)

            return topics

        except requests.exceptions.RequestException as e:
            print("❌ API 请求失败，请检查网络、服务权限或状态（请求URL及异常详情已隐藏）。")
            return []
        except json.JSONDecodeError as e:
            print("❌ API 返回了无法解析的JSON（响应详情已隐藏）。")
            return []
        except Exception as e:
            print("❌ 无法处理API响应（异常详情已隐藏）。")
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

    def save_to_json(self, topics: List[Dict], filename: Optional[str] = None) -> bool:
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
            return True
        except Exception as e:
            print("❌ 保存文件失败，请检查目录权限和磁盘空间。")
            return False

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
    try:
        client = WeiboHotSearchClient()
    except ValueError as error:
        print(f"❌ 配置错误: {error}")
        return 2
    print("🚀 正在抓取微博热搜...\n")
    topics = client.fetch_hot_search()

    if topics:
        client.display_topics(topics, limit=20)
        if not client.save_to_json(topics):
            return 1
        print(f"\n✅ 成功获取 {len(topics)} 条热搜话题")
        return 0
    else:
        print("\n❌ 未能获取热搜数据，请检查 API 端点或网络连接")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
