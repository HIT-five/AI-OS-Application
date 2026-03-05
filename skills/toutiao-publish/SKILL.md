---
name: toutiao-publish
version: 2.0.0
description: 今日头条内容自动发布技能，支持微头条和文章发布
author: HIT-five
tags: [toutiao, publish, selfmedia, automation]
dependencies:
  - python>=3.8
  - selenium
  - undetected-chromedriver
  - xvfb (Linux)
tools:
  - jimeng-image (可选，用于生成配图)
verified: true
verified_date: 2026-03-05
---

# 今日头条自动发布技能

## 功能描述

自动发布内容到今日头条平台，支持：
- **微头条发布**：短文+配图，适合日常内容
- **文章发布**：长文+封面，适合深度内容

## 核心脚本

| 脚本 | 用途 | 特点 |
|------|------|------|
| `publish_v2.py` | 微头条发布 | 短文，无标题栏 |
| `publish_article_v2.py` | 文章发布 | 长文，有标题，需xvfb |

## 使用方法

### 微头条发布

```bash
cd /path/to/toutiao-publish/scripts
python3 publish_v2.py \
  --file content.txt \
  --image-prompt "配图描述，插画风格"
```

### 文章发布（推荐）

```bash
cd /path/to/toutiao-publish/scripts
xvfb-run -a python3 publish_article_v2.py \
  --title "文章标题（不超过30字）" \
  --file content.txt \
  --cover /path/to/cover.jpg
```

## 参数说明

### publish_v2.py（微头条）

| 参数 | 说明 | 必填 |
|------|------|------|
| --file | 内容文件路径 | 是 |
| --image-prompt | 即梦AI配图提示词 | 否 |

### publish_article_v2.py（文章）

| 参数 | 说明 | 必填 |
|------|------|------|
| --title | 文章标题（≤30字） | 是 |
| --file | 内容文件路径 | 是 |
| --cover | 封面图片路径 | 否 |

## 配置说明

### Cookie配置

需要准备今日头条的登录Cookie：

1. 浏览器登录 https://mp.toutiao.com/
2. 使用浏览器扩展导出Cookie为JSON格式
3. 保存到指定路径

Cookie文件格式：
```json
[
  {"name": "cookie_name", "value": "cookie_value", "domain": ".toutiao.com"},
  ...
]
```

### Cookie路径配置

在脚本中修改 `COOKIE_PATH` 变量，或使用默认路径：
```
/home/yqj/.openclaw/workspace/toutiao_mcp_server/toutiao_cookies.json
```

## 关键注意事项

### 1. 标题字数限制
⚠️ **文章标题必须≤30字**，超过会导致发布失败！

### 2. 必须使用xvfb
文章发布必须使用 `xvfb-run -a` 运行，headless模式预览弹窗无法弹出。

### 3. ChromeDriver版本
脚本使用 undetected-chromedriver，会自动匹配Chrome版本。如遇版本不匹配，检查系统Chrome版本。

### 4. 投放广告选项
脚本会自动选择"投放广告赚收益"，这是发布必须的步骤。

## 经验记录

### 2026-03-03 文章发布验证通过
- 无封面/单封面均可正常发布
- xvfb是必须的
- 标题≤30字是硬限制

### 2026-02-28 关键修复
- ChromeDriver版本匹配问题：使用 `version_main` 参数
- "无封面"点击问题：改用 ActionChains + XPath

### 最佳实践
- 正文不要用H1标题，全部用普通段落
- 单封面比无封面流量更好
- 发布前检查标题字数
