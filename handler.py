import os
import tempfile
import traceback

try:
    import runpod
    import base64
    import whisper
except Exception as e:
    print("▶ Startup failed:", str(e))
    raise

# Load Whisper model once on cold start with GPU support
device = "cuda" if whisper.cuda.is_available() else "cpu"
print("▶ CUDA available:", whisper.cuda.is_available())
print("▶ Using device:", device)

def _load_model():
    print("▶ Loading Whisper model…")
    return whisper.load_model('small', device=device)

model = _load_model()

def handler(event):
    print("▶ Handler invoked")
    inp = event.get('input', {})
    audio_b64 = inp.get('audio')
    if not audio_b64:
        return {'error': 'No audio data provided.'}

    try:
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_b64)

        # Write to temporary file
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmp.write(audio_bytes)
        tmp.flush()
        tmp.close()

        print(f"▶ Transcribing {tmp.name}…")
        result = model.transcribe(tmp.name)
        text = result.get('text', '')

        os.remove(tmp.name)
        print("▶ Transcription complete")
        return {'text': text}

    except Exception as ex:
        print("▶ Handler error:", str(ex))
        traceback.print_exc()
        return {'error': str(ex), 'trace': traceback.format_exc()}

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
