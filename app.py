from flask import Flask, request, jsonify
import yt_dlp
import whisper
import os
import uuid

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Whisper API is live"}), 200

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "Missing 'url' in request body"}), 400

    # Create unique filename
    temp_filename = f"temp_{uuid.uuid4()}.mp3"

    try:
        # Download audio using yt-dlp
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': temp_filename,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Load whisper model and transcribe
        model = whisper.load_model("base")  # You can use "tiny", "small", "medium", etc.
        result = model.transcribe(temp_filename)

        # Clean up temp file
        os.remove(temp_filename)

        return jsonify({"transcript": result["text"]})

    except Exception as e:
        # Clean up if error
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
