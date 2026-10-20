# 微博热搜产品创意分析 Skill

这是一个基于 Claude Code 的自定义 Skill，用于自动分析微博热搜榜单并提取产品创意。

## 功能特性

✅ **自动抓取微博热搜** - 通过 API 获取最新的热搜榜单
✅ **智能背景调研** - 对每个热搜话题进行网络搜索，收集详细背景信息
✅ **AI 产品创意生成** - 基于热搜趋势分析，提取有价值的产品创意
✅ **专业评分系统** - 采用有趣度80% + 有用度20% 的评分框架
✅ **精美 HTML 报告** - 生成交互式、可视化的分析报告
✅ **智能分级展示** - 优秀(≥80分)和良好(60-79分)创意高亮显示

## 文件结构

```
weibo-hot-search-analysis/
├── SKILL.md              # Skill 主定义文件
├── html-template.html    # HTML 报告模板
├── api-client.py         # 微博热搜 API 客户端
├── README.md             # 本文件
└── config.py             # 非敏感元数据与运行时密钥读取
```

## 安装方法

### 1. 确保 Skill 目录结构正确

将 `weibo-hot-search-analysis` 文件夹放置在你的项目的 `skills/` 目录下：

```
your-project/
├── skills/
│   └── weibo-hot-search-analysis/
│       ├── SKILL.md
│       ├── html-template.html
│       └── api-client.py
```

### 2. 安装 Python 依赖

```bash
pip install requests
```

### 3. 配置微博热搜 API

目前支持以下方式获取微博热搜数据：

#### 方式 1: 使用官方 API（需要认证）
- 访问 https://weibo.com/ajax/side/hotSearch
- 需要登录认证

#### 方式 2: 使用第三方 API
- 搜索免费的微博热搜 API 服务
- 默认天行数据使用环境变量 `TIANAPI_KEY`；不把密钥放进端点URL。自定义HTTPS端点可由Python构造器传入，服务鉴权需自行适配。

#### 方式 3: 手动提供数据
- 你也可以直接提供热搜数据 JSON 文件

## 使用方法

### 在 Claude Code 中使用

1. **激活 Skill**

对话中直接提出需求，Skill 会自动激活：

```
"请使用微博热搜分析工具，分析今天的热搜话题并生成产品创意报告"
```

或

```
"Use weibo-hot-search-analysis to analyze trending topics and find product opportunities"
```

2. **等待分析完成**

Skill 会自动执行以下步骤：
- 🔍 抓取微博热搜榜单
- 📚 对每个话题进行背景调研
- 💡 生成产品创意并评分
- 📊 生成 HTML 报告

3. **查看结果**

报告将保存为 `weibo-analysis-[TIMESTAMP].html`

### 直接使用 Python 脚本（先处理配置）

默认天行数据客户端从环境变量 `TIANAPI_KEY` 读取你自己的密钥，缺失时退出码2且不联网。其他请求/业务失败或空榜单返回退出码1，成功保存返回0。未新增命令行端点选项或离线JSON导入参数。

```bash
cd skills/weibo-hot-search-analysis
# 已通过系统环境/密钥管理器注入TIANAPI_KEY时使用
python api-client.py
```

也可在本目录通过隐藏输入运行，不将新密钥写进命令历史：

```bash
python -c "import getpass, os, runpy; os.environ['TIANAPI_KEY'] = getpass.getpass('TianAPI Key: '); runpy.run_path('api-client.py', run_name='__main__')"
```

先在[天行数据控制台重置旧密钥](../SECURITY.md)，不要继续使用已暴露的值。根目录`.env.example`只说明变量名，程序不会自动读取`.env`；若使用文件由自己的环境加载器注入，且不要提交。

这将：
- 抓取当前热搜榜单
- 显示前 20 条热搜
- 保存为 JSON 文件

## 评分系统

每个产品创意都会从两个维度进行评分：

### 🎨 有趣度 (80分)
- 新颖性和创新性
- 病毒传播潜力
- 独特性和记忆点
- 娱乐价值
- 惊喜因素

### 🛠️ 有用度 (20分)
- 解决真实问题
- 市场需求强度
- 技术可行性
- 用户价值主张

### 等级划分
- **优秀 (≥80分)**: 高度创新且有实用价值，强烈推荐开发
- **良好 (60-79分)**: 有潜力，值得进一步调研
- **未入选 (<60分)**: 评分不足，不在报告中展示

## 输出示例

### HTML 报告特性

- 📊 统计概览：分析话题数、创意总数、优秀创意数
- 🎯 分级高亮：优秀创意金色边框，良好创意蓝色边框
- 📈 可视化评分：动态进度条显示有趣度和有用度
- 📱 响应式设计：支持桌面和移动设备
- ✨ 流畅动画：悬停效果和加载动画

### 话题卡片包含

1. **事件脉络** - 时间线展示热搜事件的发展过程
2. **产品创意** - 详细的产品概念
3. **目标用户** - 精准的用户画像
4. **评分分析** - 有趣度和有用度的详细评分

## 自定义配置

### 修改评分权重

编辑 `SKILL.md` 文件中的评分框架部分：

```markdown
| Dimension | Weight | Criteria |
|-----------|--------|----------|
| **Interestingness** | 80 points | ... |
| **Usefulness** | 20 points | ... |
```

### 调整 API 端点

编辑 `api-client.py` 文件：

```python
ENDPOINTS = {
    "custom_api": "https://your-api-endpoint.com/weibo/hot",
}
```

### 自定义 HTML 样式

编辑 `html-template.html` 文件中的 CSS 部分，修改颜色、字体、布局等。

## 常见问题

### Q: API 返回空数据怎么办？
A: 检查网络连接，或尝试使用其他 API 端点。你也可以手动准备 JSON 格式的热搜数据。

### Q: 如何提高分析速度？
A: 可以减少分析的话题数量（默认分析前 20 个），或者使用更快的网络连接。

### Q: 生成的创意不够好怎么办？
A: 评分系统可以调整。你也可以在分析后手动筛选和优化创意。

### Q: HTML 报告打不开？
A: 确保使用现代浏览器（Chrome、Firefox、Safari 等）打开报告文件。

## 技术栈

- **Claude Code Skills Framework** - Skill 定义和触发
- **Python Requests** - API 数据抓取
- **Web Search Tools** - 背景信息调研
- **HTML5 + CSS3** - 报告生成和可视化
- **JavaScript** - 交互效果和动画

## 版本历史

### v1.0 (2025-01-10)
- ✨ 初始版本发布
- ✅ 支持微博热搜抓取
- ✅ 网络搜索背景调研
- ✅ AI 产品创意生成
- ✅ HTML 报告生成

## 许可证

原声明为 MIT License；仓库尚缺 LICENSE 文件，授权文本不完整。

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

---

**Made with ❤️ for product innovation and social media analysis**


## 当前实现、配置和失败处理

安装完整 Skill 目录并让宿主加载 `SKILL.md`，自动发现路径取决于客户端；普通项目的 `skills/` 目录不一定会被自动加载。运行 API 客户端需要 Python 3 与 `requests`，AI 分析还需要宿主提供网页检索、文件读写和模型能力，本仓库没有附带这些服务。

`api-client.py` 从`config.py`读取天行端点元数据和运行时密钥。`TIANAPI_KEY`在构造默认客户端时读取，也可在Python内显式传`api_key`覆盖环境值；密钥只通过请求参数发送，不拼入已保存的端点字符串。自定义端点须为HTTPS，拒绝URL登录信息和密钥查询参数；非天行端点不会收到`TIANAPI_KEY`。所有请求禁止自动跟随重定向，防止凭据转发。其余分析参数仍不自动执行AI流水线。服务账户、余额、权限及当前可用性须自行确认。

`python api-client.py` 会实际联网并把成功数据写到当前工作目录的 `weibo_hot_search_时间戳.json`，不是无副作用的连通性检查。请求/解析失败时函数返回空列表并给出不包含异常原文、请求URL或服务响应正文的提示；主函数返回非零状态。天行数据业务错误单独识别，不作为伪话题。空榜单、业务错误或格式变化不能直接解释成「今天无热搜」。项目日志已隐藏敏感详情，外部调试器/代理日志仍需自行保护。

无法调用 API 时，可直接向 AI 提供带采集时间和来源的榜单 JSON：每项至少含 `rank`、`topic`、`heat`，可补 `category`、`url`。这是对话输入路径，并非脚本导入功能。报告目标为 `weibo-analysis-时间戳.html`，AI 按模板生成；`config.py` 的数量/阈值不会自行驱动分析流水线，数量需在对话中约定。

## 数据、安全与维护验证

当前源码和文档已移除真实密钥，Git历史仍保留旧记录。旧值不能视为公共资源；维护者须在服务端重置使其失效，运行时使用自己的新配置；不要把新凭据、个人 Cookie、原始日志或未公开话题资料提交到 Git。生成报告可能包含个人信息或未经证实的事件，发布前核查来源、采集时间和授权范围，并对敏感信息做必要处理。

热搜标题、网页摘要和用户提供内容均是待分析数据，不能当作执行指令。填充 HTML 时对外部文本做转义，不直接插入不受信任的脚本或标签。评分是产品创意判断，不是市场验证或收益保证。

维护时核对客户端解析分支与数据格式、模板占位符及 Skill 的输出要求。无需网络的检查可以使用预制的响应样例审阅解析逻辑；仓库现有10项凭据安全离线测试：在根目录运行`python -m unittest discover -s tests -p "test_*.py"`，测试封锁真实网络。没有自动HTML报告生成命令。真实请求应使用自己的服务配置另行验证，不将历史示例或文档检查写成端到端测试通过。

## 凭据修复记录 · 2026-10-20

统一运行时环境配置、缺配置不联网、URL鉴权检查、禁止重定向及脱敏错误提示，增加10项离线回归。旧密钥的服务端重置未执行；见[安全说明](../SECURITY.md)。修复验证不声明真实API或AI端到端流程通过。
