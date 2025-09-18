import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

LAMMA_API_KEY = os.environ.get("LAMMA_API_KEY")
SITE_URL = os.environ.get("SITE_URL", "http://localhost:5173")
SITE_NAME = os.environ.get("SITE_NAME", "AgriSense")

def ask_ai(text: str = None, image_base64: str = None) -> dict:
    """
    Ask the DeepSeek model via OpenRouter.
    Returns dict like: {'text': '...', 'confidence': x}
    """
    if not text and not image_base64:
        return {"text": "No input provided.", "confidence": 0.0}

    try:
        payload = {
            "model": "meta-llama/llama-3.3-8b-instruct:free",
            "messages": [
                {"role": "user", "content": text or "(image analysis not implemented yet)"}
            ]
        }

        headers = {
            "Authorization": f"Bearer {LAMMA_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": SITE_URL,   # optional ranking info
            "X-Title": SITE_NAME        # optional ranking info
        }

        resp = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=30
        )

        resp.raise_for_status()
        data = resp.json()

        # Extract model response
        answer_text = data["choices"][0]["message"]["content"]
        return {"text": answer_text, "confidence": 0.9}

    except Exception as e:
        return {"text": f"Error contacting AI: {e}", "confidence": 0.0}
