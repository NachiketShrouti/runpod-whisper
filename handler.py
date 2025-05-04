import os
import tempfile
import traceback

# Wrapped imports to capture early startup issues
try:
    import runpod
    import base64
    import whisper
    import torch
except Exception as e:
    print("▶ Startup failed:", str(e))
    raise

# Load Whisper model on GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
print("▶ CUDA available:", torch.cuda.is_available())
print("▶ Using device:", device)
if device == "cuda":
    print("▶ CUDA device name:", torch.cuda.get_device_name(0))

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
        # Decode base64-encoded audio
        audio_bytes = base64.b64decode(audio_b64)

        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp:
            tmp.write(audio_bytes)
            tmp.flush()
            tmp_path = tmp.name

        print(f"▶ Transcribing {tmp_path}…")
        result = model.transcribe(tmp_path)
        text = result.get('text', '')

        os.remove(tmp_path)
        print("▶ Transcription complete")
        return {'text': text}

    except Exception as ex:
        print("▶ Handler error:", str(ex))
        traceback.print_exc()
        return {
            'error': str(ex),
            'trace': traceback.format_exc()
        }

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})
