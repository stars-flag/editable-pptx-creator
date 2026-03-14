# Editable PPTX Creator

让 AI Agent 将你的内容转换为可编辑的 PowerPoint 演示文稿。

## 这是什么

这是一个 AI Agent 工具。当你想做演示文稿时，只需要告诉 Agent 你的需求，Agent 就会调用这个工具帮你生成 PPTX 文件。

生成的 PPTX 是**真正可编辑的**——所有文字、形状、颜色都能在 PowerPoint 里直接修改。

## 使用流程

### 1. 配置 Agent

确保你的 Agent（如 OpenCode）已加载此 skill：

### 2. 告诉 Agent 需求

通过你配置的消息渠道（微信、Telegram、Slack、飞书等）告诉 Agent：

```
帮我做一个关于 [主题] 的可编辑 PPT
```

### 3. Agent 自动完成

Agent 会调用 skill 完成：
1. 生成 HTML 演示文稿
2. 转换为可编辑的 PPTX
3. 将文件发送给你

## 实际示例

**你**（通过微信/Telegram/飞书等）：
> 帮我根据 OpenClaw使用文档.md 生成一个可编辑的 PPT

**Agent**：
> 好的，我来帮你生成这个演示文稿。

（Agent 执行过程：
1. 读取 OpenClaw使用文档.md 内容
2. 创建 PLANNING.md 规划结构
3. 生成 HTML 演示文稿
4. 转换为可编辑 PPTX
）

**Agent**：
> 已完成！你的演示文稿已生成：
> - 文件：openclaw-guide.pptx
> - 页数：12 页
> - 风格：Business 商务风格
> 
> 所有内容都可以在 PowerPoint 中直接编辑。

## 示例对话

**你**：帮我做一个可编辑的产品介绍 PPT

**Agent**：好的，请提供文档内容或主题，我开始生成。

（完成后）

**Agent**：已生成！12 页的商务风格 PPT，包含产品概述、功能特点、使用场景等内容。文件已发送给你。

---

简单来说，你只需要：
1. 告诉 Agent 想做什么（要可编辑的 PPT）
2. 等待完成
3. 收到可编辑的 PPTX 文件
