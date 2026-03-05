# 从本地任务到应用商店：贡献者指南

> 将你在 OpenClaw 中稳定运行的任务分享给社区

## 🎯 适用场景

当你的 OpenClaw 任务满足以下条件时，可以考虑上传到应用商店：

- ✅ 已在生产环境稳定运行
- ✅ 解决了实际问题
- ✅ 具有可复用价值
- ✅ 不涉及敏感/违规内容

## 📋 贡献流程概览

```
本地任务 → 元素拆分 → 目录组织 → 文档编写 → 提交PR
```

---

## 第一步：分析任务元素

### 1.1 识别任务组成

一个完整的任务通常包含以下元素：

| 元素类型 | 说明 | 本地位置示例 |
|----------|------|--------------|
| **Skill** | 核心能力脚本 | `~/.openclaw/workspace/skills/xxx/` |
| **Prompt** | 提示词模板 | `~/.openclaw/workspace/prompts/xxx.md` |
| **Config** | 任务配置 | `~/.openclaw/workspace/configs/xxx.json` |
| **State** | 状态文件 | `~/.openclaw/workspace/configs/xxx-state.json` |
| **Dataset** | 数据集/主题库 | `~/.openclaw/workspace/configs/xxx-topics.json` |

### 1.2 绘制依赖关系

```
我的任务
├── 依赖技能1 (skill)
├── 依赖技能2 (skill)
├── 提示词模板 (prompt)
├── 主题数据集 (dataset)
└── 平台认证 (connector)
```

---

## 第二步：Fork 并克隆仓库

```bash
# 1. 在 GitHub 上 Fork 仓库
# https://github.com/HIT-five/AI-OS-Application

# 2. 克隆到本地
git clone git@github.com:你的用户名/AI-OS-Application.git
cd AI-OS-Application

# 3. 添加上游仓库
git remote add upstream git@github.com:HIT-five/AI-OS-Application.git
```

---

## 第三步：创建目录结构

根据任务类型创建对应目录：

### 3.1 技能目录

```bash
mkdir -p skills/你的技能名/{scripts,memory}
```

结构：
```
skills/你的技能名/
├── SKILL.md              # 必须：技能说明
├── config.example.json   # 必须：配置示例（脱敏）
├── 主脚本.py             # 核心脚本
├── scripts/              # 辅助脚本
│   └── *.py
├── memory/               # 经验记录
│   └── lessons.md
└── requirements.txt      # Python依赖（如有）
```

### 3.2 工作流目录

```bash
mkdir -p workflows/你的工作流名/{config,prompts,memory}
```

结构：
```
workflows/你的工作流名/
├── WORKFLOW.md           # 必须：工作流说明
├── config/
│   ├── task.md           # 任务配置说明
│   └── state.example.json # 状态文件示例
├── prompts/
│   └── *.md              # 提示词模板
└── memory/
    └── lessons.md        # 经验记录
```

### 3.3 场景目录（多工作流组合）

```bash
mkdir -p scenarios/你的场景名
```

结构：
```
scenarios/你的场景名/
├── SCENARIO.md           # 必须：场景说明
└── memory/
    └── lessons.md
```

### 3.4 数据集目录

```bash
mkdir -p datasets/你的数据集名
```

结构：
```
datasets/你的数据集名/
├── README.md             # 必须：数据集说明
├── topics.json           # 数据文件
└── schema.md             # 数据结构说明（可选）
```

---

## 第四步：复制文件（重要原则）

### ⚠️ 核心原则

1. **只复制，不移动** - 保持原目录不变
2. **脱敏处理** - 移除所有敏感信息
3. **路径通用化** - 使用相对路径或占位符

### 4.1 复制脚本

```bash
# 复制核心脚本
cp ~/.openclaw/workspace/skills/原技能/主脚本.py \
   AI-OS-Application/skills/新技能名/

# 复制辅助脚本
cp ~/.openclaw/workspace/skills/原技能/scripts/*.py \
   AI-OS-Application/skills/新技能名/scripts/
```

### 4.2 处理配置文件

**原始配置（含敏感信息）：**
```json
{
  "ak": "AKLT1234567890abcdef",
  "sk": "SKabcdefghijklmnop",
  "cookie_path": "/home/user/.openclaw/workspace/cookies.json"
}
```

**脱敏后（config.example.json）：**
```json
{
  "ak": "YOUR_ACCESS_KEY",
  "sk": "YOUR_SECRET_KEY",
  "cookie_path": "/path/to/your/cookies.json"
}
```

### 4.3 处理脚本中的硬编码路径

**修改前：**
```python
COOKIE_PATH = "/home/yqj/.openclaw/workspace/toutiao_cookies.json"
```

**修改后：**
```python
import os
# 从环境变量或配置文件读取
COOKIE_PATH = os.environ.get("TOUTIAO_COOKIE_PATH", "./cookies.json")
```

或在文档中说明需要用户自行修改路径。

---

## 第五步：编写文档

### 5.1 SKILL.md 模板

```markdown
---
name: 技能名称
version: 1.0.0
description: 一句话描述
author: 你的名字
tags: [标签1, 标签2, 标签3]
dependencies:
  - python>=3.8
  - 依赖包1
  - 依赖包2
verified: true
verified_date: YYYY-MM-DD
---

# 技能名称

## 功能描述

详细说明这个技能能做什么，解决什么问题。

## 使用方法

### 基本用法
\```bash
python3 main_script.py --param value
\```

### 参数说明

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| --param1 | 参数描述 | 是 | - |
| --param2 | 参数描述 | 否 | 默认值 |

## 配置说明

### 获取配置

1. 步骤1
2. 步骤2
3. 步骤3

### 配置文件格式

\```json
{
  "key": "说明"
}
\```

## 示例

### 示例1：基本使用
\```bash
命令示例
\```

### 示例2：高级用法
\```bash
命令示例
\```

## 注意事项

1. 注意事项1
2. 注意事项2

## 常见问题

### Q: 问题1？
A: 解答1

### Q: 问题2？
A: 解答2
```

### 5.2 WORKFLOW.md 模板

```markdown
---
name: 工作流名称
version: 1.0.0
description: 一句话描述
trigger: cron | manual | event
schedule: "*/30 * * * *"
skills:
  - 依赖技能1
  - 依赖技能2
config_files:
  - config/task.md
state_files:
  - config/state.json
verified: true
verified_date: YYYY-MM-DD
---

# 工作流名称

## 功能描述

这个工作流完成什么任务，适用于什么场景。

## 执行流程

### 步骤1：XXX
描述这一步做什么。

### 步骤2：YYY
描述这一步做什么。

### 步骤3：ZZZ
描述这一步做什么。

## 配置说明

### 必要配置

| 配置项 | 说明 | 获取方式 |
|--------|------|----------|
| 配置1 | 说明 | 获取步骤 |
| 配置2 | 说明 | 获取步骤 |

### 状态文件初始化

\```json
{
  "lastIndex": 0,
  "lastRunTime": null
}
\```

## 运行方式

### 手动运行

\```
向 OpenClaw 发送：开始执行【工作流名称】
\```

### 定时运行（OpenClaw Cron）

\```json
{
  "name": "工作流名称",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行指令内容"
  }
}
\```

## 依赖检查清单

- [ ] 技能1 已配置
- [ ] 技能2 已配置
- [ ] 必要软件已安装
- [ ] 配置文件已创建
- [ ] 状态文件已初始化

## 注意事项

1. 重要注意事项
```

### 5.3 经验记录 (memory/lessons.md)

```markdown
# 经验记录

## 问题与解决

### 问题1：问题描述
- **现象**：遇到了什么问题
- **原因**：为什么会出现
- **解决**：如何解决的
- **日期**：YYYY-MM-DD

## 最佳实践

1. **实践名称**：具体做法和原因
2. **实践名称**：具体做法和原因

## 踩坑记录

- ❌ 错误做法：描述
- ✅ 正确做法：描述
```

---

## 第六步：更新主 README

在仓库根目录的 `README.md` 中添加你的贡献：

```markdown
### 技能 (Skills)

| 技能 | 描述 | 状态 |
|------|------|------|
| [你的技能](skills/你的技能/) | 描述 | ✅ 已验证 |

### 工作流 (Workflows)

| 工作流 | 描述 | 状态 |
|--------|------|------|
| [你的工作流](workflows/你的工作流/) | 描述 | ✅ 已验证 |
```

---

## 第七步：提交 PR

### 7.1 创建分支

```bash
git checkout -b feat/你的功能名
```

### 7.2 提交变更

```bash
git add -A
git commit -m "feat: 添加XXX功能

🎯 技能 (Skills)
- skill-name: 简短描述

📋 工作流 (Workflows)  
- workflow-name: 简短描述

📊 数据集 (Datasets)
- dataset-name: 简短描述

✅ 已在生产环境验证通过"
```

### 7.3 推送并创建 PR

```bash
git push origin feat/你的功能名
```

然后在 GitHub 上创建 Pull Request。

---

## ✅ 提交前检查清单

### 文件完整性
- [ ] 每个技能有 SKILL.md
- [ ] 每个工作流有 WORKFLOW.md
- [ ] 每个场景有 SCENARIO.md
- [ ] 每个数据集有 README.md

### 安全性
- [ ] 无 API 密钥/Token
- [ ] 无个人路径硬编码
- [ ] 无 Cookie/密码
- [ ] 敏感配置有 .example 版本

### 可复现性
- [ ] 依赖列表完整
- [ ] 配置说明清晰
- [ ] 有使用示例
- [ ] 有 OpenClaw 集成说明

### 经验传承
- [ ] 包含 lessons.md
- [ ] 记录了踩坑经验
- [ ] 记录了最佳实践

---

## 💡 贡献建议

### 什么样的内容更受欢迎？

1. **解决实际问题** - 不是玩具项目
2. **文档完善** - 别人能看懂、能用起来
3. **经验丰富** - 踩过的坑都记录下来
4. **维护承诺** - 愿意回复 issue 和更新

### 命名规范

- **技能名**：`功能-动作`，如 `jimeng-image`、`toutiao-publish`
- **工作流名**：`平台-领域-动作`，如 `toutiao-health-publish`
- **场景名**：`平台-场景`，如 `toutiao-selfmedia`
- **数据集名**：`领域-类型`，如 `health-topics`

### 版本号规范

遵循语义化版本：`主版本.次版本.修订号`

- 主版本：不兼容的重大变更
- 次版本：向后兼容的功能新增
- 修订号：向后兼容的问题修复

---

## 🤝 需要帮助？

- 提交 Issue 描述你的问题
- 参考现有的技能/工作流结构
- 查看 [OpenClaw 集成指南](openclaw-integration.md)

感谢你的贡献！🎉
