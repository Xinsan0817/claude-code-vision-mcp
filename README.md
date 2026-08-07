# Image Vision MCP

为 Claude Code 部署多模态图片识别能力。通过 MCP 协议接入第三方视觉模型，让非多模态后端也能看图。

## 功能

- OCR 文字提取
- 图表解读
- 场景描述
- UI 截图分析
- 文档扫描件识别

## 支持的模型

| 模型 | BASE_URL | MODEL |
|------|----------|-------|
| Qwen3.8-Max | `dashscope.aliyuncs.com/compatible-mode/v1` | `qwen3.8-max` |
| GPT-4o | `api.openai.com/v1` | `gpt-4o` |
| GPT-4o-mini | `api.openai.com/v1` | `gpt-4o-mini` |
| Gemini 2.0 Flash | `generativelanguage.googleapis.com/v1beta/openai` | `gemini-2.0-flash` |
| 本地 Ollama | `localhost:11434/v1` | `llava:13b` |

## 快速开始

1. 修改 `scripts/vision-mcp.py` 中配置区的 `API_KEY`
2. 在 Claude Code 项目根目录创建 `.mcp.json`：

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

3. 在 `~/.claude/settings.json` 中添加 API 域名到 sandbox 白名单
4. 重启 Claude Code

## 使用

```
识别 /path/to/image.jpg 里有什么
提取这张图片的所有文字
这张图表展示了什么趋势
```

## 原理

纯 Python 标准库实现，零外部依赖。图片 base64 编码后通过 OpenAI 兼容的 `chat/completions` 接口发送给视觉模型。

## 许可

MIT
