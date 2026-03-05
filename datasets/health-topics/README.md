# 健康养生主题库

## 概述

适合中老年人群的健康养生话题集合，用于自媒体内容创作。

## 主题数量

- 总计：20个主题
- 循环发布

## 主题分类

- 日常习惯：喝水、午睡、晚餐、走路、泡脚
- 慢性病管理：高血压、糖尿病
- 器官保健：养胃、护肝、补钙、心血管、关节、眼睛
- 常见问题：失眠、便秘、血脂、骨质疏松
- 季节养生：春夏秋冬

## 使用方式

```python
import json

with open('topics.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

topics = data['topics']
next_topic = topics[current_index % len(topics)]
```

## 扩展建议

如需扩展主题库，可按以下类别添加：
- 中医养生
- 运动健身
- 心理健康
- 营养膳食
