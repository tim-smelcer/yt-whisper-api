from flask import Flask, request, jsonify
import subprocess
import os
import requests
import uuid

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def download_audio(video_id):
    filename = f"{uuid.uuid4()}.mp3"
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "mp3",
        "-o", filename,
        f"https://www.youtube.com/watch?v={video_id}"
    ]
    subprocess.run(command, check=True)
    return filename

def transcribe_with_whisper(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
            files={"file": f},
            data={"model": "whisper-1"}
        )
    return response.json().get("text", "")

@app.route("/transcribe")
def transcribe():
    video_id = request.args.get("v")
    if not video_id:
        return jsonify({"error": "Missing video ID"}), 400
    try:
        filename = download_audio(video_id)
        transcript = transcribe_with_whisper(filename)
        os.remove(filename)
        return jsonify({"transcript": transcript})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
