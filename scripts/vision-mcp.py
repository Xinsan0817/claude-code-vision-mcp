#!/usr/bin/env python3
"""
MCP Server — 多模态识图
纯 Python 标准库，零外部依赖。

模型可替换：
  - Qwen3.8-Max / Qwen-VL 系列
  - GPT-4o / GPT-4V
  - Gemini 2.0 Flash / Pro
  - Claude 3.5 Sonnet / Opus 4
  - 任何支持 image_url 输入的 OpenAI 兼容 API
"""

import sys, json, base64, urllib.request, urllib.error, os, mimetypes

# ========== 配置区 ==========
API_KEY = "your-api-key-here"
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
MODEL = "qwen3.8-max"
# =============================


def log(msg):
    print(f"[vision-mcp] {msg}", file=sys.stderr, flush=True)


def encode_image(image_path: str) -> str:
    """读取图片并转为 base64 data URL"""
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type or not mime_type.startswith("image/"):
        mime_type = "image/png"
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{data}"


def call_vision(image_path: str, prompt: str) -> str:
    """发送图片+文本给视觉模型，返回文字描述"""
    data_url = encode_image(image_path)
    body = {
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": data_url}},
                {"type": "text", "text": prompt},
            ],
        }],
        "max_tokens": 4096,
    }
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise RuntimeError(f"API HTTP {e.code}: {error_body}")


# ========== MCP 协议处理 ==========

def handle_initialize(params: dict) -> dict:
    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "vision-mcp", "version": "1.0.0"},
    }


def handle_list_tools(params: dict) -> dict:
    return {
        "tools": [{
            "name": "recognize_image",
            "description": (
                "使用多模态视觉模型识别图片内容。"
                "传入图片文件路径和可选的提示词，返回图片的文字描述。"
                "适用于：OCR文字提取、图表解读、场景描述、文档扫描件识别、UI截图分析等。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "图片文件的绝对路径，支持 PNG/JPG/GIF/WEBP/BMP",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "可选的识别提示词。例如：'提取所有文字'、'描述这个图表'",
                    },
                },
                "required": ["image_path"],
            },
        }]
    }


def handle_call_tool(params: dict) -> dict:
    args = params.get("arguments", {})
    image_path = args["image_path"]
    prompt = args.get("prompt", "请详细描述这张图片的内容。")

    if not os.path.exists(image_path):
        return {
            "content": [{"type": "text", "text": f"错误：文件不存在 — {image_path}"}],
            "isError": True,
        }

    try:
        result = call_vision(image_path, prompt)
        return {"content": [{"type": "text", "text": result}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"识别失败：{e}"}],
            "isError": True,
        }


METHODS = {
    "initialize": handle_initialize,
    "tools/list": handle_list_tools,
    "tools/call": handle_call_tool,
}


def main():
    log("Vision MCP server starting...")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue

        req_id = request.get("id")
        method = request.get("method")
        handler = METHODS.get(method)

        if handler:
            try:
                result = handler(request.get("params", {}))
                response = {"jsonrpc": "2.0", "id": req_id, "result": result}
            except Exception as e:
                response = {
                    "jsonrpc": "2.0", "id": req_id,
                    "error": {"code": -32603, "message": str(e)},
                }
        else:
            response = {
                "jsonrpc": "2.0", "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"},
            }

        sys.stdout.write(json.dumps(response) + "\n")
        sys.stdout.flush()


if __name__ == "__main__":
    main()
