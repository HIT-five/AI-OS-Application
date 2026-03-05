---
name: toutiao-health-publish
version: 1.0.0
description: 今日头条健康养生内容定时发布工作流
trigger: cron | manual
schedule: "*/30 * * * *"
skills:
  - jimeng-image
  - toutiao-publish
tools:
  - web_search (OpenClaw内置)
config_files:
  - config/task.md
  - config/settings.json
state_files:
  - config/state.json
verified: true
verified_date: 2026-03-05
---

# 今日头条健康养生内容定时发布工作流

## 功能描述

自动生成并发布健康养生类文章到今日头条，包括：
- 从主题列表获取下一个待发布主题
- 搜索该主题的权威研究资料
- 按模板撰写700-1000字文章
- 生成AI配图
- 自动发布到今日头条
- 更新发布状态

## 执行流程

### 步骤1：获取下一个主题
从状态文件读取 `lastIndex`，获取主题列表中下一个待发布的主题。

### 步骤2：搜索权威研究
使用 web_search 搜索该主题的：
- 最新医学研究
- 权威专家观点
- 健康指南建议

### 步骤3：撰写文章
按照 `prompts/article-template.md` 模板撰写：
- 故事化开头
- 权威背书
- 核心内容（分点列举）
- 实操建议
- 互动引导

### 步骤4：生成封面
调用 jimeng-image 技能生成与主题相关的封面图片。

### 步骤5：发布文章
调用 toutiao-publish 技能发布文章：
```bash
xvfb-run -a python3 publish_article_v2.py \
  --title "文章标题" \
  --file article.txt \
  --cover cover.jpg
```

### 步骤6：更新状态
更新状态文件：
- lastIndex + 1
- lastPublishTime
- lastPublishStatus
- publishedToday 列表

## 配置说明

### settings.json
```json
{
  "topicSource": "内置20个主题循环",
  "publishInterval": "30分钟",
  "imageStyle": "中老年健康生活场景，暖色调，写实摄影"
}
```

### state.json
```json
{
  "lastIndex": 0,
  "publishedToday": [],
  "lastPublishTime": null,
  "lastPublishStatus": null,
  "lastPublishError": null
}
```

## 主题列表（内置20个）

1. 早起喝水的正确方式
2. 午睡的最佳时长
3. 晚餐吃太饱的危害
4. 走路锻炼的正确姿势
5. 睡前泡脚的注意事项
6. 高血压患者饮食禁忌
7. 糖尿病人水果选择
8. 养胃的日常习惯
9. 护肝的生活方式
10. 补钙的正确方法
... (共20个主题循环)

## 启动/停止指令

**启动（手动）**：
```
开始执行【今日头条健康养生内容定时发布任务】
```

**启动（定时）**：
使用 OpenClaw cron 工具配置定时任务。

**停止**：
```
停止执行【今日头条健康养生内容定时发布任务】
```

## OpenClaw Cron 配置

```json
{
  "name": "toutiao-health-publish",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行今日头条健康养生内容定时发布任务..."
  }
}
```

## 注意事项

1. **标题字数**：必须≤30字
2. **发布频率**：建议间隔30分钟以上
3. **Cookie有效性**：定期检查Cookie是否过期
4. **主题循环**：20个主题循环发布，避免重复

## 依赖检查清单

- [ ] jimeng-image 技能已配置（config.json）
- [ ] toutiao-publish 技能已配置（Cookie）
- [ ] xvfb 已安装（Linux）
- [ ] Chrome/Chromium 已安装
- [ ] 状态文件已初始化
