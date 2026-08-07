---
name: image-vision
description: 为 Claude Code 部署多模态图片识别能力。通过 MCP 协议接入第三方视觉模型（如 Qwen-VL、GPT-4o、Gemini 等），实现 OCR 文字提取、图表解读、场景描述、文档扫描件识别、UI 截图分析等功能。适用于已将 Claude Code 后端换为非多模态模型（如 DeepSeek）的用户。
metadata:
  category: ai-tools
  difficulty: 简单
  time_to_deploy: 5 分钟
requires:
  bins: [python3]
install: |
  本 Skill 使用 Python 3 标准库，无需安装任何额外依赖。

  确保系统已安装 Python 3：
  ```
  python3 --version
  ```

  将 MCP 脚本复制到你想要的位置：
  ```
  cp skills/image-vision/scripts/vision-mcp.py /your/path/vision-mcp.py
  chmod +x /your/path/vision-mcp.py
  ```

  修改脚本中的 API_KEY 和 BASE_URL 为你自己的模型配置。
---

# 多模态图片识别 Skill

## 这个 Skill 做什么

当 Claude Code 的后端模型不支持多模态（如 DeepSeek），这个 Skill 通过 MCP 协议接入第三方视觉模型，让 Claude Code 重新获得"看图"能力。

## 工作流程

```
用户发送图片路径 ──► Claude Code ──► MCP recognize_image ──► 视觉模型 API ──► 返回文字描述
```

## 支持的视觉模型

| 模型 | 配置 |
|------|------|
| Qwen3.8-Max | `BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1`, `MODEL=qwen3.8-max` |
| GPT-4o | `BASE_URL=https://api.openai.com/v1`, `MODEL=gpt-4o` |
| GPT-4o-mini | `BASE_URL=https://api.openai.com/v1`, `MODEL=gpt-4o-mini` |
| Gemini 2.0 Flash | `BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai`, `MODEL=gemini-2.0-flash` |
| Claude 3.5 Sonnet | `BASE_URL=https://api.anthropic.com/v1`, `MODEL=claude-3-5-sonnet-20241022` |
| 任意兼容 OpenAI 接口的模型 | 修改 BASE_URL 和 MODEL 即可 |

## 部署步骤

### 1. 创建 MCP 服务器脚本

将 `scripts/vision-mcp.py` 复制到你的工作目录，修改配置区：

```python
API_KEY = "your-api-key"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"  # 改为你的服务
MODEL = "qwen3.8-max"  # 改为你的模型
```

### 2. 注册 MCP 服务

在项目根目录创建 `.mcp.json`：

```json
{
  "mcpServers": {
    "vision-mcp": {
      "command": "python3",
      "args": ["/path/to/vision-mcp.py"],
      "env": {}
    }
  }
}
```

### 3. 配置网络白名单

编辑 `~/.claude/settings.json`，在 `sandbox.network.allowedDomains` 中添加 API 域名。例如 Qwen 需要添加 `dashscope.aliyuncs.com`。

### 4. 重启 Claude Code

完全退出（Cmd+Q / Ctrl+C）后重新启动，MCP 服务会自动加载。

## 使用方式

部署完成后，直接将图片保存为本地文件，然后对 Claude Code 说：

- "识别 /path/to/image.jpg 里有什么"
- "提取这张图片里的所有文字 /path/to/screenshot.png"
- "这张图表展示了什么趋势 /path/to/chart.png"
- "分析这个 UI 截图的布局 /path/to/ui.png"

Claude Code 会自动调用 `recognize_image` 工具。

## 触发词 & 场景

当用户的请求符合以下特征时，主动使用此 Skill：
- 用户提到"识别"、"看图"、"OCR"、"提取文字"等关键词
- 用户提供了图片文件路径并希望获取内容描述
- 用户上传了图表、截图、扫描件需要解读
- 用户询问如何让 Claude Code 支持多模态

## 核心 MCP 脚本

See: [scripts/vision-mcp.py](scripts/vision-mcp.py)

纯 Python 标准库实现，零外部依赖。通过 `image_url` 格式将图片 base64 编码后发送给任意 OpenAI 兼容的 Chat Completions API。
