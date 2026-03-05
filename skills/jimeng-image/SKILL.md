---
name: jimeng-image
version: 1.0.0
description: 即梦AI图片生成技能，基于火山引擎视觉服务
author: HIT-five
tags: [ai, image, generation, volcengine, jimeng]
dependencies:
  - python>=3.8
  - requests
verified: true
verified_date: 2026-03-05
---

# 即梦AI图片生成技能

## 功能描述

使用火山引擎即梦AI API生成高质量图片，支持多种图片比例，适用于：
- 自媒体文章配图
- 封面图片生成
- 创意内容配图

## 使用方法

### 命令行使用

```bash
cd /path/to/jimeng-image
python3 jimeng_image.py --prompt "图片描述" --output /path/to/output.jpg
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| --prompt | 图片描述（必填） | - |
| --output | 输出路径（可选） | 自动生成 |
| --ratio | 图片比例（可选） | 1:1 |

### 支持的比例

- 1:1 (正方形)
- 16:9 (横版)
- 9:16 (竖版)
- 4:3
- 3:4

## 配置说明

需要创建 `config.json` 配置文件：

```json
{
  "ak": "你的火山引擎AccessKey",
  "sk": "你的火山引擎SecretKey"
}
```

### 获取密钥

1. 注册火山引擎账号：https://www.volcengine.com/
2. 开通即梦AI服务
3. 创建AccessKey：控制台 → 密钥管理

## 示例

### 生成自媒体配图

```bash
python3 jimeng_image.py \
  --prompt "温馨家庭场景，父母陪伴孩子阅读，暖色调，写实摄影" \
  --output cover.jpg
```

### 生成健康主题配图

```bash
python3 jimeng_image.py \
  --prompt "中老年人晨练太极，公园场景，阳光明媚，健康活力" \
  --output health_cover.jpg
```

## 注意事项

1. **必须在技能目录运行**：脚本需要读取同目录下的 `config.json`
2. **生成需要时间**：通常5-30秒，建议设置300秒超时
3. **提示词技巧**：
   - 描述具体场景
   - 指定风格（写实/插画/卡通）
   - 指定色调（暖色/冷色）
   - 避免敏感内容

## 经验记录

### 2026-02-12 验证通过
- API调用正常
- 图片质量满足自媒体使用需求
- 生成时间约5-15秒

### 最佳实践
- 封面图片建议使用 16:9 比例
- 配图建议使用 1:1 比例
- 提示词包含"写实摄影"效果更自然
