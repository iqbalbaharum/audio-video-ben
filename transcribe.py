import os
import base64
import httpx

env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()

wav_path = "/Users/iqbalbaharum/Projects/ai/audio-video-ben/malayoutput14_audio_raw.wav"

with open(wav_path, "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode("utf-8")

response = httpx.post(
    url="https://openrouter.ai/api/v1/audio/transcriptions",
    headers={
        "Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "openai/whisper-large-v3-turbo",
        "input_audio": {
            "data": audio_b64,
            "format": "wav",
        },
    },
)
response.raise_for_status()
result = response.json()

output_path = "/Users/iqbalbaharum/Projects/ai/audio-video-ben/transcript.txt"
with open(output_path, "w") as f:
    f.write(result["text"])

print(f"Transcript written to {output_path}")
print("Content:")
print(result["text"])
