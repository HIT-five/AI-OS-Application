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
| **Skill** | 单一能力模块，包含指令、脚本、依赖 | `weather-skill`, `web-search-skill` |
| **Tool** | 可调用的工具/API封装 | `jimeng-image`, `toutiao-publish` |
| **Memory** | 技能构建过程中的经验记忆 | 调试经验、最佳实践、踩坑记录 |
| **Prompt** | 可复用的提示词模板 | 文章写作模板、代码生成模板 |
| **Script** | 自动化脚本片段 | Python脚本、Shell脚本 |

### 宏观元素（应用级）

| 元素 | 描述 | 示例 |
|------|------|------|
| **Workflow** | 完整的任务工作流 | "自媒体内容发布流程" |
| **Scenario** | 完整应用场景定义 | "今日头条自动运营" |
| **Config** | 工作流运行配置 | Cookie、API Key、定时规则 |
| **Context** | 场景记忆与上下文 | 发布进度、主题列表状态 |
| **Agent** | 预配置的Agent角色 | "育儿内容创作者" |

### 补充元素

| 元素 | 描述 | 示例 |
|------|------|------|
| **Connector** | 平台/服务连接器 | WeChat、Feishu、Telegram |
| **Template** | 项目/场景模板 | "自媒体矩阵模板" |
| **Dataset** | 训练/参考数据集 | 主题库、关键词库 |
| **Evaluation** | 效果评估方案 | 发布成功率、内容质量评分 |

## 🏗️ 目录结构

```
AI-OS-Application/
├── skills/                 # 技能模块
│   ├── skill-name/
│   │   ├── SKILL.md       # 技能说明
│   │   ├── scripts/       # 脚本文件
│   │   ├── prompts/       # 提示词模板
│   │   └── memory/        # 经验记忆
│   └── ...
├── tools/                  # 工具封装
│   ├── tool-name/
│   │   ├── README.md
│   │   ├── config.json
│   │   └── src/
│   └── ...
├── workflows/              # 工作流定义
│   ├── workflow-name/
│   │   ├── WORKFLOW.md    # 流程说明
│   │   ├── config/        # 配置文件
│   │   ├── state/         # 状态文件
│   │   └── prompts/       # 流程提示词
│   └── ...
├── scenarios/              # 应用场景
│   ├── scenario-name/
│   │   ├── SCENARIO.md    # 场景说明
│   │   ├── workflows/     # 包含的工作流
│   │   ├── skills/        # 依赖的技能
│   │   └── memory/        # 场景记忆
│   └── ...
├── connectors/             # 平台连接器
├── templates/              # 项目模板
├── datasets/               # 数据集
└── docs/                   # 文档
    ├── getting-started.md
    ├── skill-development.md
    └── workflow-design.md
```

## 🔧 元素规范

### Skill 规范
```yaml
# SKILL.md 头部元信息
name: skill-name
version: 1.0.0
description: 技能描述
author: 作者
tags: [标签1, 标签2]
dependencies:
  - python>=3.8
  - requests
tools:
  - tool-name
```

### Workflow 规范
```yaml
# WORKFLOW.md 头部元信息
name: workflow-name
version: 1.0.0
description: 工作流描述
trigger: cron | manual | event
schedule: "0 */30 * * * *"  # 如果是定时触发
skills:
  - skill-1
  - skill-2
config_files:
  - config/settings.json
  - config/state.json
```

## 🚀 快速开始

### 安装技能
```bash
# 克隆仓库
git clone git@github.com:HIT-five/AI-OS-Application.git

# 进入技能目录
cd AI-OS-Application/skills/your-skill

# 按照 SKILL.md 说明配置
```

### 运行工作流
```bash
# 进入工作流目录
cd AI-OS-Application/workflows/your-workflow

# 配置必要参数
cp config/settings.example.json config/settings.json

# 按照 WORKFLOW.md 说明执行
```

## 🤝 贡献指南

欢迎贡献新的技能、工具、工作流！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/new-skill`)
3. 按照规范添加内容
4. 提交 PR

## 📄 License

MIT License

---

> 💡 AI-OS-Application: 让AI Agent的能力像乐高积木一样可组合、可复用、可分享
