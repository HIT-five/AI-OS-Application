---
name: toutiao-selfmedia
version: 1.0.0
description: 今日头条自媒体自动化运营场景
workflows:
  - toutiao-health-publish
  - toutiao-childedu-publish
skills:
  - jimeng-image
  - toutiao-publish
datasets:
  - health-topics
  - childedu-topics
verified: true
verified_date: 2026-03-05
---

# 今日头条自媒体自动化运营场景

## 场景描述

一个完整的今日头条自媒体自动化运营方案，包括：
- 内容自动生成（基于主题库 + AI写作）
- 配图自动生成（即梦AI）
- 定时自动发布
- 状态追踪管理

## 包含工作流

| 工作流 | 内容领域 | 主题数 | 发布频率 |
|--------|----------|--------|----------|
| toutiao-health-publish | 健康养生 | 20 | 30分钟 |
| toutiao-childedu-publish | 育儿教育 | 800 | 30分钟 |

## 依赖技能

| 技能 | 用途 |
|------|------|
| jimeng-image | AI配图生成 |
| toutiao-publish | 内容发布 |

## 部署步骤

### 1. 安装依赖

```bash
# Python依赖
pip install selenium undetected-chromedriver requests

# 系统依赖（Ubuntu/Debian）
sudo apt-get install xvfb chromium-browser
```

### 2. 配置技能

#### 配置 jimeng-image
```bash
cd skills/jimeng-image
cp config.example.json config.json
# 编辑 config.json，填入火山引擎密钥
```

#### 配置 toutiao-publish
1. 浏览器登录 https://mp.toutiao.com/
2. 导出Cookie为JSON格式
3. 保存到指定路径

### 3. 初始化工作流状态

```bash
# 健康养生工作流
cd workflows/toutiao-health-publish/config
cp state.example.json state.json

# 育儿教育工作流
cd workflows/toutiao-childedu-publish/config
cp state.example.json state.json
```

### 4. 配置 OpenClaw 定时任务

```bash
# 使用 OpenClaw cron 工具添加定时任务
# 参考各工作流的 WORKFLOW.md 中的 cron 配置
```

## 运行方式

### 手动运行（测试）

向 OpenClaw 发送指令：
```
开始执行【今日头条育儿教育内容定时发布任务】
```

### 定时运行（生产）

配置 OpenClaw cron 任务后自动执行。

### 停止运行

```
停止执行【今日头条育儿教育内容定时发布任务】
```

或禁用 cron 任务。

## 监控与维护

### 状态检查
- 查看 `state.json` 了解发布进度
- 检查 `lastPublishStatus` 确认是否成功
- 查看 `publishedToday` 了解今日发布内容

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 发布失败 | Cookie过期 | 重新导出Cookie |
| 标题超限 | >30字 | 检查标题生成逻辑 |
| 图片生成失败 | API限流 | 增加重试或间隔 |
| 浏览器启动失败 | Chrome版本 | 更新Chrome |

### 日志位置
- 发布截图：技能目录下的 debug_*.png
- OpenClaw日志：按OpenClaw配置

## 扩展建议

### 添加新的内容领域
1. 创建新的主题数据集
2. 创建新的文章模板
3. 复制工作流并修改配置

### 多平台发布
可扩展到其他平台：
- 微信公众号
- 百家号
- 知乎

### 内容优化
- 接入数据分析，了解哪类内容更受欢迎
- 根据反馈调整主题优先级
- A/B测试不同的标题风格

## 成本估算

| 项目 | 费用 | 说明 |
|------|------|------|
| 即梦AI | 按量付费 | 约0.1元/张 |
| OpenClaw | 按API调用 | 取决于模型 |
| 服务器 | 自备 | 需要Linux环境 |

## 注意事项

1. **遵守平台规则**：避免发布频率过高
2. **内容质量**：定期检查生成内容质量
3. **Cookie维护**：定期更新登录状态
4. **备份状态**：定期备份state.json
