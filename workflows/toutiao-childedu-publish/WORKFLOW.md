---
name: toutiao-childedu-publish
version: 1.0.0
description: 今日头条育儿教育内容定时发布工作流
trigger: cron | manual
schedule: "*/30 * * * *"
skills:
  - jimeng-image
  - toutiao-publish
tools:
  - web_search (OpenClaw内置)
datasets:
  - childedu-topics (800个主题)
config_files:
  - config/task.md
  - config/settings.json
state_files:
  - config/state.json
verified: true
verified_date: 2026-03-05
---

# 今日头条育儿教育内容定时发布工作流

## 功能描述

自动生成并发布育儿教育类文章到今日头条，特点：
- 800个主题的大型主题库
- 按年龄段分类（0-3岁/3-6岁/小学/青春期）
- 按类型分类（情绪/习惯/学习/社交等）
- 支持循环发布

## 执行流程

### 步骤1：获取下一个主题
从状态文件读取 `lastIndex`，解析主题库获取下一个主题：

```python
topics = []
for age_group, categories in data['育儿教育话题图谱'].items():
    for category, topic_list in categories.items():
        topics.extend(topic_list)
next_topic = topics[lastIndex]
```

### 步骤2：搜索权威研究
使用 web_search 搜索该主题的：
- 儿童发展心理学研究
- 儿科医生/教育专家观点
- 权威育儿指南

### 步骤3：撰写文章
按照 `prompts/article-template.md` 模板撰写700-1000字文章：
- 场景引入（班级观察/门诊数据/家长咨询）
- 权威背书（研究结论/专家观点）
- 核心内容（emoji + 小标题形式）
- 实操建议（按年龄给出具体方法）
- 互动引导

### 步骤4：生成封面
调用 jimeng-image 技能：
```bash
cd /path/to/jimeng-image
python3 jimeng_image.py \
  --prompt "与主题相关的配图描述，温馨家庭场景，暖色调，写实摄影" \
  --output cover.jpg
```

### 步骤5：发布文章
调用 toutiao-publish 技能：
```bash
cd /path/to/toutiao-publish/scripts
xvfb-run -a python3 publish_article_v2.py \
  --title "文章标题（≤30字）" \
  --file article.txt \
  --cover cover.jpg
```

### 步骤6：更新状态
```json
{
  "lastIndex": lastIndex + 1,
  "publishedToday": [..., "新发布的标题"],
  "lastPublishTime": "ISO时间戳",
  "lastPublishStatus": "success"
}
```

如果 lastIndex >= 800，重置为 0 循环发布。

## 配置说明

### settings.json
```json
{
  "topicSource": "datasets/childedu-topics/topics.json",
  "totalTopics": 800,
  "publishInterval": "30分钟",
  "imageStyle": "亲子场景，温馨家庭，暖色调，写实摄影"
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

## 主题库结构

```
育儿教育话题图谱
├── 0-3岁（宝宝期）
│   ├── 情绪类（25个）
│   ├── 习惯类（25个）
│   ├── 认知类（25个）
│   └── 社交类（25个）
├── 3-6岁（幼儿期）
│   ├── 情绪类（25个）
│   ├── 习惯类（25个）
│   ├── 学习类（25个）
│   └── 社交类（25个）
├── 小学阶段
│   ├── 学习类（50个）
│   ├── 习惯类（50个）
│   ├── 情绪类（50个）
│   └── 社交类（50个）
└── 青春期
    ├── 情绪类（50个）
    ├── 学习类（50个）
    ├── 社交类（50个）
    └── 亲子关系（50个）
```

## 启动/停止指令

**启动（手动）**：
```
开始执行【今日头条育儿教育内容定时发布任务】
```

**停止**：
```
停止执行【今日头条育儿教育内容定时发布任务】
```

## OpenClaw Cron 配置

```json
{
  "name": "toutiao-childedu-publish",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行今日头条育儿教育内容定时发布任务...",
    "timeoutSeconds": 900
  }
}
```

## 关键注意事项

1. **标题字数**：必须≤30字，这是硬限制！
2. **即梦AI运行位置**：必须cd到技能目录运行
3. **xvfb必须**：文章发布必须用xvfb-run
4. **超时设置**：建议900秒（15分钟）
5. **循环逻辑**：lastIndex >= 800 时重置为 0

## 依赖检查清单

- [ ] jimeng-image 技能已配置
- [ ] toutiao-publish 技能已配置
- [ ] 主题库文件已就位（800个主题）
- [ ] xvfb 已安装
- [ ] Chrome/Chromium 已安装
- [ ] Cookie 有效
