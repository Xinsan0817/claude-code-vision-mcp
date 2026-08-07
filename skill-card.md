## Description:

为 Claude Code 部署多模态图片识别能力。通过 MCP 协议接入第三方视觉模型，让非多模态后端也能"看图"。

模型无关设计——支持 Qwen-VL、GPT-4o、Gemini、Claude 等任意 OpenAI 兼容接口。

## Publisher:

Self-deployed · Local MCP Server

## Use Case:

Claude Code 后端为非多模态模型（如 DeepSeek）的用户，需要 OCR 文字提取、图表解读、场景描述、UI 截图分析、文档扫描件识别等图片理解能力。

纯 Python 标准库实现，零外部依赖，5 分钟部署完成。

## Deployment Geography for Use:

Global — 可选择使用国内的阿里云 DashScope、国外的 OpenAI/Gemini API，或本地部署的视觉模型。

## Known Risks and Mitigations:

Risk: 图片数据通过 base64 编码发送至第三方 API。
Mitigation: 使用前确认 API 服务商的数据隐私政策；敏感图片建议使用本地模型。

## Reference(s):

- [阿里云 DashScope](https://dashscope.aliyun.com)
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Gemini API](https://ai.google.dev/gemini-api/docs/vision)

## Skill Output:

**Output Type(s):** text, markdown
**Output Format:** 文字描述，按用户指定的提示词格式返回
