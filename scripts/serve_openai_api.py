"""
MiniAgent OpenAI-Compatible API Server

Provides /v1/chat/completions endpoint compatible with:
FastGPT, Open-WebUI, Dify, and any OpenAI SDK client.

Usage:
    python scripts/serve_openai_api.py --model ./checkpoints/sft_512.pth --port 8080
"""

import os
import sys
import json
import time
import argparse
import torch
from http.server import HTTPServer, BaseHTTPRequestHandler

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL = None
TOKENIZER = None
DEVICE = "cpu"


class OpenAIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/v1/chat/completions":
            self._chat_completions()
        else:
            self._respond(404, {"error": "Not found"})

    def do_GET(self):
        if self.path == "/v1/models":
            self._respond(200, {
                "data": [{"id": "miniagent", "object": "model", "owned_by": "itallstartedwithaidea"}]
            })
        elif self.path == "/health":
            self._respond(200, {"status": "ok", "model_loaded": MODEL is not None})
        else:
            self._respond(404, {"error": "Not found"})

    def _chat_completions(self):
        length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(length))

        messages = body.get("messages", [])
        temperature = body.get("temperature", 0.7)
        max_tokens = body.get("max_tokens", 512)

        # Build prompt from messages
        prompt = ""
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            prompt += f"<s>{role}\n{content}</s>"
        prompt += "<s>assistant\n"

        # Generate
        if MODEL is not None and TOKENIZER is not None:
            input_ids = torch.tensor([TOKENIZER.encode(prompt)], device=DEVICE)
            with torch.no_grad():
                output = MODEL.generate(input_ids, max_new_tokens=max_tokens,
                                        temperature=temperature)
            response_text = TOKENIZER.decode(output[0].tolist(), skip_special_tokens=True)
        else:
            user_msg = messages[-1]["content"] if messages else ""
            response_text = f"MiniAgent received: '{user_msg}'. Model not loaded — train one first."

        result = {
            "id": f"chatcmpl-miniagent-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "miniagent",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": response_text},
                "finish_reason": "stop",
            }],
            "usage": {"prompt_tokens": len(prompt), "completion_tokens": len(response_text), "total_tokens": len(prompt) + len(response_text)},
        }
        self._respond(200, result)

    def _respond(self, status, data):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        pass  # Suppress default logging


def main():
    global MODEL, TOKENIZER, DEVICE

    parser = argparse.ArgumentParser(description="MiniAgent OpenAI API Server")
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    args = parser.parse_args()

    DEVICE = args.device

    if args.model and os.path.exists(args.model):
        from model.model_miniagent import MiniAgentModel
        checkpoint = torch.load(args.model, map_location=DEVICE)
        MODEL = MiniAgentModel(checkpoint["config"]).to(DEVICE)
        MODEL.load_state_dict(checkpoint["model"])
        MODEL.eval()
        try:
            from transformers import AutoTokenizer
            TOKENIZER = AutoTokenizer.from_pretrained("./model/tokenizer", trust_remote_code=True)
        except Exception:
            pass
        print(f"Model loaded: {MODEL.count_params():.1f}M params on {DEVICE}")

    server = HTTPServer((args.host, args.port), OpenAIHandler)
    print(f"\nMiniAgent API server running at http://{args.host}:{args.port}")
    print(f"  /v1/chat/completions  — Chat endpoint (OpenAI compatible)")
    print(f"  /v1/models            — Model listing")
    print(f"  /health               — Health check")
    print(f"\nConnect from FastGPT/Open-WebUI/Dify using: http://localhost:{args.port}")
    print("Press Ctrl+C to stop.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")


if __name__ == "__main__":
    main()
