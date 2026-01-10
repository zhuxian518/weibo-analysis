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
└── example-output.html   # 示例输出报告（待生成）
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
- 在 `api-client.py` 中配置你的 API 端点

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

### 直接使用 Python 脚本

如果你想先测试 API 是否正常工作：

```bash
cd skills/weibo-hot-search-analysis
python api-client.py
```

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

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。

---

**Made with ❤️ for product innovation and social media analysis**
