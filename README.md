# 微博热搜产品创意分析

这是一个 AI Skill、Python 热搜数据客户端和 HTML 报告模板集合。Python 脚本只获取并保存榜单，不会独立完成背景调研或生成产品报告；后续分析由宿主 AI 按 Skill 执行。

## 入口与目录

- [安装、使用与限制](weibo-hot-search-analysis/README.md)
- [Skill 指令](weibo-hot-search-analysis/SKILL.md)：触发条件、背景研究、80/20 评分与报告输出。
- [API 客户端](weibo-hot-search-analysis/api-client.py)：获取并标准化榜单。
- [配置参考](weibo-hot-search-analysis/config.py)：端点元数据、环境变量密钥读取及供AI参考的分析参数。
- [HTML 模板](weibo-hot-search-analysis/html-template.html)：由 AI 填充报告。
- 仓库根目录的带时间戳 HTML 是历史示例，不是今天的榜单或实时分析。

## 使用边界

客户端已移除硬编码密钥，默认从环境变量 `TIANAPI_KEY` 读取；缺失或占位配置会在联网前退出。不要将密钥写进源码、URL或提交记录；`.env.example`仅是示例，不自动加载。请先读[安全修复与旧密钥重置](SECURITY.md)。历史泄露值仍需在服务端重置，删除当前代码不能让旧值失效。

离线回归：`python -m unittest discover -s tests -p "test_*.py"`（先安装`requests`）。10项测试封锁真实网络，不使用服务密钥。

原 README/Skill 声明 MIT，但仓库未附 LICENSE 文件，授权文本尚不完整；第三方数据及报告素材不因此获得再分发授权。
