# OpenClaw 集成指南

本文档说明如何将 AI-OS-Application 中的技能、工作流、场景接入 OpenClaw 运行。

## 什么是 OpenClaw

OpenClaw 是一个 AI Agent 运行时框架，提供：
- 多渠道消息接入（WhatsApp/Telegram/Discord等）
- 工具调用能力（文件/Shell/浏览器等）
- 定时任务（Cron）
- 会话管理

## 接入方式

### 方式一：技能接入

将技能放入 OpenClaw 的 skills 目录：

```bash
# 复制技能到 OpenClaw 工作空间
cp -r AI-OS-Application/skills/jimeng-image ~/.openclaw/workspace/skills/
cp -r AI-OS-Application/skills/toutiao-publish ~/.openclaw/workspace/skills/
```

OpenClaw 会自动识别 `SKILL.md` 并在需要时加载。

### 方式二：工作流接入

工作流通过 OpenClaw 的 Cron 功能实现定时执行：

```bash
# 复制工作流配置
cp -r AI-OS-Application/workflows/toutiao-health-publish ~/.openclaw/workspace/workflows/
```

然后通过 OpenClaw 配置 Cron 任务。

### 方式三：场景接入

场景是多个工作流的组合，部署步骤：

1. 安装所有依赖技能
2. 配置所有工作流
3. 设置定时任务

## Cron 任务配置

### 配置格式

```json
{
  "name": "任务名称",
  "schedule": {
    "kind": "every",
    "everyMs": 1800000
  },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "执行指令...",
    "timeoutSeconds": 900
  },
  "delivery": {
    "mode": "announce"
  }
}
```

### 参数说明

| 参数 | 说明 |
|------|------|
| name | 任务名称 |
| schedule.kind | 调度类型：at/every/cron |
| schedule.everyMs | 间隔毫秒数（every类型） |
| sessionTarget | main 或 isolated |
| payload.kind | agentTurn 或 systemEvent |
| payload.message | 执行的指令内容 |
| payload.timeoutSeconds | 超时时间 |
| delivery.mode | 结果通知：none/announce |

### 添加任务

通过 OpenClaw 的 cron 工具添加：

```
向 OpenClaw 发送：
添加定时任务：
{任务配置JSON}
```

或直接调用 cron action=add。

### 管理任务

```
# 查看任务列表
cron action=list

# 启用/禁用任务
cron action=update jobId=xxx patch={"enabled": true/false}

# 手动执行一次
cron action=run jobId=xxx

# 删除任务
cron action=remove jobId=xxx
```

## 示例：配置育儿教育发布任务

### 1. 安装技能

```bash
# 确保技能在 OpenClaw 工作空间
ls ~/.openclaw/workspace/skills/jimeng-image/
ls ~/.openclaw/workspace/skills/toutiao-publish/
```

### 2. 准备配置文件

```bash
# 即梦AI配置
cat ~/.openclaw/workspace/skills/jimeng-image/config.json
# 确保有 ak 和 sk

# Cookie配置
ls ~/.openclaw/workspace/toutiao_mcp_server/toutiao_cookies.json
# 确保Cookie有效
```

### 3. 初始化状态文件

```bash
# 创建状态文件
cat > ~/.openclaw/workspace/configs/childedu-topic-state.json << 'EOF'
{
  "lastIndex": 0,
  "publishedToday": [],
  "lastPublishTime": null,
  "lastPublishStatus": null,
  "lastPublishError": null
}
EOF
```

### 4. 添加Cron任务

向 OpenClaw 发送：

```
添加定时任务，每30分钟执行一次育儿教育内容发布：

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

### 5. 验证

```
# 手动执行一次测试
开始执行【今日头条育儿教育内容定时发布任务】

# 检查状态
查看定时任务状态
```

## 工作流指令模板

### 育儿教育发布指令

```
执行今日头条育儿教育内容定时发布任务（带封面）：

1. 读取状态文件 `/path/to/childedu-topic-state.json` 获取 lastIndex
2. 读取主题内容文件，解析获取下一个主题
3. 使用 web_search 搜索该主题的权威研究
4. 按模板撰写700-1000字文章
5. 保存文章到临时文件
6. 生成封面图片（即梦AI）
7. 调用发布脚本（xvfb-run）
8. 更新状态文件
9. 报告发布结果

⚠️ 注意：标题必须≤30字
```

### 健康养生发布指令

```
执行今日头条健康养生内容定时发布任务：

1. 读取状态文件获取下一个主题
2. web_search 搜索权威研究
3. 按模板撰写文章
4. 生成配图
5. 发布到今日头条
6. 更新状态
7. 报告结果
```

## 故障排查

### 任务未执行
- 检查任务是否启用：`cron action=list`
- 检查 OpenClaw 是否运行

### 发布失败
- 检查 Cookie 是否过期
- 检查标题是否超过30字
- 查看截图了解失败位置

### 图片生成失败
- 检查即梦AI配置
- 检查API余额
- 增加超时时间

## 最佳实践

1. **先手动测试**：添加定时任务前，先手动执行验证流程
2. **设置合理间隔**：避免发布频率过高
3. **监控状态**：定期检查 state.json
4. **备份配置**：定期备份 Cookie 和状态文件
5. **日志记录**：保留发布截图用于排查问题
