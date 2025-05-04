import os
import tempfile

# Wrap imports so startup errors appear in logs
try:
    import runpod
    import base64
    import whisper
except Exception as e:
    print("▶ Startup failed:", str(e))
    raise

# Load Whisper model once at cold start
def _load_model():
    print("▶ Loading Whisper model…")
    # Choose from 'base', 'small', 'medium', 'large'
    return whisper.load_model('small')

model = _load_model()

def handler(event):
    """
    Expects event['input']['audio'] as a base64-encoded audio file.
    Returns the transcribed text.
    """
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

        # Clean up
        os.remove(tmp.name)
        print("▶ Transcription complete")
        return {'text': text}

    except Exception as ex:
        print("▶ Handler error:", str(ex))
        return {'error': str(ex)}

if __name__ == '__main__':
    # Start the Serverless worker
    runpod.serverless.start({'handler': handler})
