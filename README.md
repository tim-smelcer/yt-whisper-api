# yt-whisper-api

A simple Flask API that:
1. Downloads audio from a YouTube video using `yt-dlp`
2. Converts it to mp3
3. Sends it to OpenAI Whisper for transcription

## Usage

Deploy to Render, and hit:

```
/transcribe?v=VIDEO_ID
```

Set `OPENAI_API_KEY` as an environment variable.
