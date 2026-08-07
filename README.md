# Claude Code External Vision MCP

> 在 Claude Code 中调用外部多模态视觉模型，让非多模态后端（如 DeepSeek）也能看图。
> Call external multimodal vision models from within Claude Code, giving non-multimodal backends (like DeepSeek) the ability to see.

---

## Features / 功能

- OCR text extraction / 文字提取
- Chart & diagram interpretation / 图表解读
- Scene description / 场景描述
- UI screenshot analysis / UI 截图分析
- Scanned document recognition / 文档扫描件识别

## Supported Models / 支持的模型

| Model | BASE_URL | MODEL |
|-------|----------|-------|
| Qwen3.8-Max | `dashscope.aliyuncs.com/compatible-mode/v1` | `qwen3.8-max` |
| GPT-4o | `api.openai.com/v1` | `gpt-4o` |
| GPT-4o-mini | `api.openai.com/v1` | `gpt-4o-mini` |
| Gemini 2.0 Flash | `generativelanguage.googleapis.com/v1beta/openai` | `gemini-2.0-flash` |
| Local Ollama / 本地 | `localhost:11434/v1` | `llava:13b` |
| Any OpenAI-compatible API | any | any |

> Model-agnostic — any API that accepts `image_url` in Chat Completions works.

## Quick Start / 快速开始

1. Edit `API_KEY` in `scripts/vision-mcp.py`
2. Register in Claude Code `.mcp.json`:

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

3. Add the API domain to `~/.claude/settings.json` sandbox allowlist
4. Restart Claude Code

## Usage / 使用

```
What's in /path/to/image.jpg
识别 /path/to/image.jpg 里有什么
Extract all text from this image
这张图表展示了什么趋势
Describe this UI layout
```

## How It Works / 原理

Pure Python stdlib, zero external dependencies. The image is base64-encoded and sent via OpenAI-compatible `chat/completions` API to the vision model. Claude Code communicates with the MCP server via JSON-RPC over stdio.

纯 Python 标准库实现，零外部依赖。图片 base64 编码后通过 OpenAI 兼容接口发送给视觉模型。

## License / 许可

MIT
