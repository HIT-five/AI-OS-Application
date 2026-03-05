# 工作流设计指南

## 工作流结构

```
workflow-name/
├── WORKFLOW.md        # 必须：工作流说明
├── config/            # 配置文件
│   ├── settings.json  # 运行配置
│   └── state.json     # 状态文件
├── prompts/           # 流程中使用的提示词
│   └── step1.md
├── scripts/           # 自动化脚本
│   └── executor.py
└── memory/            # 运行记忆
    └── run-log.md
```

## WORKFLOW.md 规范

```markdown
---
name: workflow-name
version: 1.0.0
description: 工作流描述
trigger: cron | manual | event
schedule: "*/30 * * * *"  # cron表达式（如果是定时触发）
skills:
  - skill-1
  - skill-2
tools:
  - tool-1
config_files:
  - config/settings.json
state_files:
  - config/state.json
---

# 工作流名称

## 功能描述
这个工作流完成什么任务。

## 执行流程

### 步骤1：XXX
描述步骤1做什么。

### 步骤2：YYY
描述步骤2做什么。

### 步骤3：ZZZ
描述步骤3做什么。

## 配置说明

### settings.json
```json
{
  "key1": "说明",
  "key2": "说明"
}
```

### state.json
```json
{
  "lastIndex": 0,
  "lastRunTime": null
}
```

## 启动/停止指令

**启动**：
「开始执行【工作流名称】」

**停止**：
「停止执行【工作流名称】」

## 注意事项
使用注意事项。
```

## 状态管理

工作流需要管理状态以支持：
- 断点续传
- 进度追踪
- 错误恢复

### 状态文件示例

```json
{
  "lastIndex": 35,
  "lastRunTime": "2026-03-05T09:22:00",
  "lastStatus": "success",
  "lastError": null,
  "history": [
    {"time": "...", "topic": "...", "status": "success"},
    {"time": "...", "topic": "...", "status": "success"}
  ]
}
```

## 触发方式

### 1. 手动触发
用户发送指令启动。

### 2. 定时触发（Cron）
使用 cron 工具定时执行。

```json
{
  "name": "工作流名称",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行工作流指令..."
  }
}
```

### 3. 事件触发
响应特定事件执行。

## 错误处理

工作流应该处理：
- 网络错误：重试机制
- 配置错误：清晰的错误提示
- 状态错误：自动恢复或人工介入

## 设计原则

1. **幂等性**：重复执行不会产生副作用
2. **可恢复**：失败后可以从断点继续
3. **可观测**：有清晰的日志和状态
4. **可配置**：关键参数可配置
5. **低耦合**：技能之间松耦合
