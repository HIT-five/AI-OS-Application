# AI-OS-Application

> 🚀 AI-OS 下一代应用商店 - 重新定义AI Agent的能力生态

## ⚡ 核心能力

<table>
<tr>
<td width="50%" valign="top">

### 📤 上传到商店

**将你的稳定任务分享给社区**

```bash
# 1. Fork 仓库
# 2. 按流程拆分任务元素
# 3. 提交 PR
```

👉 [**完整上传指南**](docs/contribution-workflow.md)

- 7步标准流程
- 完整文档模板
- 脱敏处理规范
- 提交前检查清单

</td>
<td width="50%" valign="top">

### 📥 下载到本地

**一键获取社区能力，对接 OpenClaw**

```bash
# 1. 克隆仓库
git clone https://github.com/HIT-five/AI-OS-Application.git

# 2. 复制技能到 OpenClaw
cp -r skills/技能名 ~/.openclaw/workspace/skills/

# 3. 按文档配置即可使用
```

👉 [**快速接入指南**](docs/openclaw-integration.md)

</td>
</tr>
</table>

---

## 🎯 核心理念

AI-OS-Application 不是传统意义上的"应用商店"，而是一个**AI Agent能力生态系统**。

| 传统应用商店 | AI-OS 应用商店 |
|-------------|---------------|
| 下载独立App | 获取可组合的能力模块 |
| 安装 = 复制文件 | 安装 = Agent学习新技能 |
| 运行 = 启动进程 | 运行 = 多能力协同工作 |

---

## 📦 商店内容

### 技能 (Skills) - 原子能力

| 技能 | 描述 | 状态 |
|------|------|------|
| [jimeng-image](skills/jimeng-image/) | 即梦AI图片生成 | ✅ 已验证 |
| [toutiao-publish](skills/toutiao-publish/) | 今日头条内容发布 | ✅ 已验证 |

### 工作流 (Workflows) - 任务编排

| 工作流 | 描述 | 状态 |
|--------|------|------|
| [toutiao-health-publish](workflows/toutiao-health-publish/) | 健康养生内容定时发布 | ✅ 已验证 |
| [toutiao-childedu-publish](workflows/toutiao-childedu-publish/) | 育儿教育内容定时发布 | ✅ 已验证 |

### 场景 (Scenarios) - 完整方案

| 场景 | 描述 | 状态 |
|------|------|------|
| [toutiao-selfmedia](scenarios/toutiao-selfmedia/) | 今日头条自媒体自动化运营 | ✅ 已验证 |

### 数据集 (Datasets) - 内容资源

| 数据集 | 描述 | 数量 |
|--------|------|------|
| [health-topics](datasets/health-topics/) | 健康养生主题库 | 20个 |
| [childedu-topics](datasets/childedu-topics/) | 育儿教育主题库 | 800个 |

---

## 🚀 快速开始

### 方式一：使用现有能力（下载）

```bash
# 1. 克隆仓库
git clone https://github.com/HIT-five/AI-OS-Application.git
cd AI-OS-Application

# 2. 选择需要的技能/工作流
ls skills/
ls workflows/

# 3. 复制到 OpenClaw 工作空间
cp -r skills/jimeng-image ~/.openclaw/workspace/skills/
cp -r workflows/toutiao-health-publish ~/.openclaw/workspace/workflows/

# 4. 按各模块的 SKILL.md / WORKFLOW.md 配置
# 5. 开始使用！
```

详见 👉 [OpenClaw 集成指南](docs/openclaw-integration.md)

### 方式二：分享你的能力（上传）

```bash
# 1. Fork 本仓库

# 2. 分析你的任务涉及的元素
#    - Skills（技能脚本）
#    - Prompts（提示词模板）
#    - Configs（配置文件）
#    - Datasets（数据集）

# 3. 按目录规范组织文件

# 4. 编写说明文档

# 5. 提交 PR
```

详见 👉 [贡献者指南：从本地任务到应用商店](docs/contribution-workflow.md)

---

## 📁 目录结构

```
AI-OS-Application/
├── skills/                 # 技能模块（原子能力）
│   ├── jimeng-image/      
│   └── toutiao-publish/   
├── workflows/              # 工作流（任务编排）
│   ├── toutiao-health-publish/
│   └── toutiao-childedu-publish/
├── scenarios/              # 场景（完整方案）
│   └── toutiao-selfmedia/
├── datasets/               # 数据集
│   ├── health-topics/
│   └── childedu-topics/
├── connectors/             # 平台连接器
│   └── toutiao/
├── docs/                   # 📚 文档
│   ├── getting-started.md
│   ├── contribution-workflow.md  # ⭐ 上传指南
│   ├── openclaw-integration.md   # ⭐ 下载/接入指南
│   ├── skill-development.md
│   └── workflow-design.md
└── templates/              # 项目模板
```

---

## 📚 文档导航

| 文档 | 说明 |
|------|------|
| [📤 上传指南](docs/contribution-workflow.md) | 将本地任务分享到商店的完整流程 |
| [📥 接入指南](docs/openclaw-integration.md) | 从商店下载并对接 OpenClaw |
| [快速开始](docs/getting-started.md) | 了解基本概念 |
| [技能开发](docs/skill-development.md) | 如何开发新技能 |
| [工作流设计](docs/workflow-design.md) | 如何设计工作流 |

---

## 🤝 参与贡献

我们欢迎任何形式的贡献！

- 🐛 发现问题？[提交 Issue](https://github.com/HIT-five/AI-OS-Application/issues)
- 💡 有新想法？[发起讨论](https://github.com/HIT-five/AI-OS-Application/discussions)
- 🎁 分享能力？[查看上传指南](docs/contribution-workflow.md)

详见 [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📄 License

MIT License

---

<p align="center">
  <b>💡 AI-OS-Application</b><br>
  让AI Agent的能力像乐高积木一样可组合、可复用、可分享
</p>
