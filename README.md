# Audio to Text Transcriber

Transcribe WAV audio files to text using OpenAI Whisper via OpenRouter.

## Files

| File | Description |
|------|-------------|
| `transcribe.py` | Standalone script — reads `.env` for the API key, transcribes `malayoutput14_audio_raw.wav`, writes `transcript.txt` |
| `audio_transcriber_server.py` | MCP server — exposes `transcribe_audio` as a tool for use with MCP clients (opencode, Claude Desktop, etc.) |
| `.env` | Stores `OPENROUTER_API_KEY` (for standalone script only) |

## Prerequisites

- Python 3.12+
- `OPENROUTER_API_KEY` — set in your environment or MCP client config

## Usage

### Standalone

```bash
pip install httpx
python transcribe.py
```

Output is written to `transcript.txt`.

### MCP Server

Run as a stdio-based MCP server:

```bash
python audio_transcriber_server.py
```

Add to your MCP client config (e.g., `opencode.json`):

```json
{
  "mcpServers": {
    "audio-transcriber": {
      "command": "python3",
      "args": ["/path/to/audio_transcriber_server.py"],
      "env": {
        "OPENROUTER_API_KEY": "sk-or-..."
      }
    }
  }
}
```

Then call:

```
transcribe_audio(file_url="/path/to/audio.wav") -> transcript text
```

## License

MIT
