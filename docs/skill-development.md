# 技能开发指南

## 技能结构

一个标准的技能目录结构：

```
skill-name/
├── SKILL.md           # 必须：技能说明文档
├── scripts/           # 可选：脚本文件
│   ├── main.py
│   └── utils.py
├── prompts/           # 可选：提示词模板
│   └── template.md
├── config/            # 可选：配置文件
│   └── config.json
├── memory/            # 可选：经验记忆
│   └── lessons.md
└── requirements.txt   # 可选：Python依赖
```

## SKILL.md 规范

```markdown
---
name: skill-name
version: 1.0.0
description: 简短描述
author: 作者名
tags: [tag1, tag2]
dependencies:
  - python>=3.8
  - 其他依赖
tools:
  - 依赖的工具名
verified: true  # 是否已验证
verified_date: 2026-03-05
---

# 技能名称

## 功能描述
详细说明这个技能能做什么。

## 使用方法
如何使用这个技能。

## 配置说明
需要配置什么。

## 示例
具体使用示例。

## 注意事项
使用时需要注意的问题。

## 经验记录
调试过程中的经验教训。
```

## 经验记忆格式

`memory/lessons.md` 记录技能开发和使用过程中的经验：

```markdown
# 经验记录

## 问题与解决

### 问题1：XXX报错
- **现象**：描述问题现象
- **原因**：分析原因
- **解决**：解决方案
- **日期**：2026-03-05

### 问题2：性能问题
...

## 最佳实践

1. 实践1：描述
2. 实践2：描述

## 踩坑记录

- ❌ 错误做法：XXX
- ✅ 正确做法：YYY
```

## 提示词模板格式

`prompts/template.md` 定义可复用的提示词：

```markdown
# 模板名称

## 用途
说明这个模板用于什么场景。

## 变量
- `{topic}`: 主题
- `{style}`: 风格

## 模板内容

你是一个{style}的写作助手，请围绕"{topic}"撰写一篇文章。

要求：
1. 要求1
2. 要求2
...
```

## 发布检查清单

发布技能前，确保：

- [ ] SKILL.md 完整且格式正确
- [ ] 所有脚本可正常运行
- [ ] 依赖列表完整
- [ ] 配置文件有示例
- [ ] 经验记忆有价值
- [ ] 已在本地测试通过
