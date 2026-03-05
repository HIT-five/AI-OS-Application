# AI-OS-Application

> 🚀 AI-OS 下一代应用商店 - 重新定义AI Agent的能力生态

## 🎯 核心理念

AI-OS-Application 不是传统意义上的"应用商店"，而是一个**AI Agent能力生态系统**。

在这个生态中：
- **应用 = 能力组合** - 不再是独立的App，而是可组合、可复用的能力模块
- **安装 = 学习** - Agent通过"安装"获得新能力，本质是学习新技能
- **运行 = 协作** - 多个能力模块协同工作，完成复杂任务

## 📦 生态元素

### 微观元素（原子级）

| 元素 | 描述 | 示例 |
|------|------|------|
| **Skill** | 单一能力模块 | `jimeng-image`, `toutiao-publish` |
| **Tool** | 可调用的工具/API封装 | API客户端、自动化脚本 |
| **Memory** | 技能构建过程中的经验记忆 | 调试经验、最佳实践 |
| **Prompt** | 可复用的提示词模板 | 文章写作模板 |

### 宏观元素（应用级）

| 元素 | 描述 | 示例 |
|------|------|------|
| **Workflow** | 完整的任务工作流 | `toutiao-health-publish` |
| **Scenario** | 完整应用场景 | `toutiao-selfmedia` |
| **Dataset** | 数据集 | `health-topics`, `childedu-topics` |
| **Connector** | 平台连接器 | `toutiao` |

## 🗂️ 当前内容

### 技能 (Skills)

| 技能 | 描述 | 状态 |
|------|------|------|
| [jimeng-image](skills/jimeng-image/) | 即梦AI图片生成 | ✅ 已验证 |
| [toutiao-publish](skills/toutiao-publish/) | 今日头条内容发布 | ✅ 已验证 |

### 工作流 (Workflows)

| 工作流 | 描述 | 状态 |
|--------|------|------|
| [toutiao-health-publish](workflows/toutiao-health-publish/) | 健康养生内容定时发布 | ✅ 已验证 |
| [toutiao-childedu-publish](workflows/toutiao-childedu-publish/) | 育儿教育内容定时发布 | ✅ 已验证 |

### 场景 (Scenarios)

| 场景 | 描述 | 状态 |
|------|------|------|
| [toutiao-selfmedia](scenarios/toutiao-selfmedia/) | 今日头条自媒体自动化运营 | ✅ 已验证 |

### 数据集 (Datasets)

| 数据集 | 描述 | 数量 |
|--------|------|------|
| [health-topics](datasets/health-topics/) | 健康养生主题库 | 20个 |
| [childedu-topics](datasets/childedu-topics/) | 育儿教育主题库 | 800个 |

## 🚀 快速开始

### 1. 克隆仓库

```bash
git clone git@github.com:HIT-five/AI-OS-Application.git
cd AI-OS-Application
```

### 2. 选择使用方式

#### 使用单个技能
```bash
cd skills/jimeng-image
# 阅读 SKILL.md，按说明配置和使用
```

#### 运行工作流
```bash
cd workflows/toutiao-childedu-publish
# 阅读 WORKFLOW.md，配置后通过 OpenClaw 执行
```

#### 部署完整场景
```bash
cd scenarios/toutiao-selfmedia
# 阅读 SCENARIO.md，按步骤部署
```

### 3. 接入 OpenClaw

参考 [OpenClaw 集成指南](docs/openclaw-integration.md)

## 📁 目录结构

```
AI-OS-Application/
├── skills/                 # 技能模块
│   ├── jimeng-image/      # 即梦AI图片生成
│   └── toutiao-publish/   # 今日头条发布
├── workflows/              # 工作流定义
│   ├── toutiao-health-publish/    # 健康养生发布
│   └── toutiao-childedu-publish/  # 育儿教育发布
├── scenarios/              # 应用场景
│   └── toutiao-selfmedia/ # 自媒体运营场景
├── datasets/               # 数据集
│   ├── health-topics/     # 健康主题库
│   └── childedu-topics/   # 育儿主题库
├── connectors/             # 平台连接器
│   └── toutiao/           # 今日头条连接配置
├── docs/                   # 文档
│   ├── getting-started.md
│   ├── skill-development.md
│   ├── workflow-design.md
│   └── openclaw-integration.md
└── templates/              # 项目模板（待添加）
```

## 🔧 开发指南

- [快速开始](docs/getting-started.md)
- [技能开发指南](docs/skill-development.md)
- [工作流设计指南](docs/workflow-design.md)
- [OpenClaw 集成指南](docs/openclaw-integration.md)
- [📦 贡献者指南：从本地任务到应用商店](docs/contribution-workflow.md)

## 🤝 贡献指南

欢迎贡献新的技能、工具、工作流！详见 [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License

---

> 💡 AI-OS-Application: 让AI Agent的能力像乐高积木一样可组合、可复用、可分享
