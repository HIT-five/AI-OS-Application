# 今日头条育儿教育内容定时发布任务配置

## 任务标识
- **任务名称**: toutiao-health-publish
- **任务类型**: 定时发布
- **间隔时间**: 约30分钟（25-35分钟随机）

## 主题轮换列表（循环使用，确保差异性）

主题内容文件：`/home/yqj/.openclaw/workspace/configs/childedu-topic-content.json`

## 主题状态追踪
使用文件记录：`/home/yqj/.openclaw/workspace/configs/childedu-topic-state.json`

```json
{
  "lastIndex": 0,
  "topics": [
    "0-1岁宝宝频繁哭闹，不是饿了而是这5个信号",
    ...
  ],
  "publishedToday": []
}
```

## 执行流程

每次定时触发时：
1. 读取主题状态，获取下一个主题
2. 使用 web_search 搜索该主题的最新权威研究
3. 按照 toutiao-childedu-article.md 模板撰写文章
4. 调用 publish_article_v2.py 发布（带即梦AI配图）
5. 更新主题索引，记录发布时间
6. 向用户报告发布结果

## 启停指令

- **启动**: 「开始执行【今日头条育儿教育内容定时发布任务】」
- **停止**: 「结束执行【今日头条育儿教育内容定时发布任务】」
