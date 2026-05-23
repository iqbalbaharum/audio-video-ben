import os
import base64
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("audio-transcriber")

@mcp.tool()
def transcribe_audio(file_url: str) -> str:
    """Transcribe an audio file to text using OpenAI Whisper via OpenRouter."""
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set in environment")

    with open(file_url, "rb") as f:
        audio_b64 = base64.b64encode(f.read()).decode("utf-8")

    response = httpx.post(
        url="https://openrouter.ai/api/v1/audio/transcriptions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/whisper-large-v3-turbo",
            "input_audio": {"data": audio_b64, "format": "wav"},
        },
    )
    response.raise_for_status()
    return response.json()["text"]

if __name__ == "__main__":
    mcp.run(transport="stdio")
