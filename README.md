# 微博热搜产品创意分析

这是一个 AI Skill、Python 热搜数据客户端和 HTML 报告模板集合。Python 脚本只获取并保存榜单，不会独立完成背景调研或生成产品报告；后续分析由宿主 AI 按 Skill 执行。

## 入口与目录

- [安装、使用与限制](weibo-hot-search-analysis/README.md)
- [Skill 指令](weibo-hot-search-analysis/SKILL.md)：触发条件、背景研究、80/20 评分与报告输出。
- [API 客户端](weibo-hot-search-analysis/api-client.py)：获取并标准化榜单。
- [配置参考](weibo-hot-search-analysis/config.py)：分析参数；当前客户端不导入此配置。
- [HTML 模板](weibo-hot-search-analysis/html-template.html)：由 AI 填充报告。
- 仓库根目录的带时间戳 HTML 是历史示例，不是今天的榜单或实时分析。

## 使用边界

运行前先阅读子目录 README 的凭据与数据说明。当前源码存在硬编码 API Key 的历史配置，本仓库不提供可共享的服务凭据或可用性保证；不要直接使用默认配置发请求。维护者需在独立代码修复中移除硬编码并处理密钥生命周期。本次文档维护不测试凭据、不改变源码或调用外部服务。

原 README/Skill 声明 MIT，但仓库未附 LICENSE 文件，授权文本尚不完整；第三方数据及报告素材不因此获得再分发授权。
