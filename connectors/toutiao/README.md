# 今日头条连接器

## 概述

今日头条平台连接配置，用于内容发布自动化。

## 认证方式

今日头条创作者平台使用 Cookie 认证。

### 获取Cookie

1. 浏览器登录 https://mp.toutiao.com/
2. 使用浏览器扩展（如 EditThisCookie）导出Cookie
3. 保存为JSON格式

### Cookie格式

```json
[
  {
    "name": "cookie_name",
    "value": "cookie_value",
    "domain": ".toutiao.com",
    "path": "/",
    "expires": 1234567890,
    "httpOnly": false,
    "secure": false
  },
  ...
]
```

### Cookie存储位置

建议存储在：
```
~/.openclaw/workspace/toutiao_mcp_server/toutiao_cookies.json
```

## 平台限制

| 限制项 | 说明 |
|--------|------|
| 文章标题 | ≤30字 |
| 发布频率 | 建议≥30分钟间隔 |
| 封面图片 | 支持无封面/单封面/三封面 |
| 内容审核 | 自动审核，敏感内容会被拒绝 |

## API端点

| 功能 | URL |
|------|-----|
| 创作者平台 | https://mp.toutiao.com/ |
| 文章发布 | https://mp.toutiao.com/profile_v4/graphic/publish |
| 内容管理 | https://mp.toutiao.com/profile_v4/graphic/articles |

## 注意事项

1. Cookie会定期失效，需要重新获取
2. 频繁发布可能触发风控
3. 内容需符合平台规范
4. 建议使用固定IP操作

## 故障排查

### 登录失效
- 重新获取Cookie
- 检查Cookie格式是否正确

### 发布被拒
- 检查内容是否含敏感词
- 检查标题是否过长
- 查看平台通知了解拒绝原因
