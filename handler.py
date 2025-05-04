import runpod
import base64
import whisper
import tempfile
import os

def handler(event):
    """
    Expects event['input']['audio'] as a base64-encoded audio file.
    Returns the transcribed text.
    """
    inp = event.get('input', {})
    audio_b64 = inp.get('audio')
    if not audio_b64:
        return {'error': 'No audio data provided.'}

    try:
        # Decode base64 audio data
        audio_bytes = base64.b64decode(audio_b64)

        # Write to temporary file
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        tmp_file.write(audio_bytes)
        tmp_file.flush()
        tmp_file.close()

        # Transcribe with Whisper model
        # Model is loaded globally for efficiency
        result = model.transcribe(tmp_file.name)
        text = result.get('text', '')

        # Clean up
        os.remove(tmp_file.name)

        return {'text': text}
    except Exception as e:
        return {'error': str(e)}

# Load Whisper model once at cold start
def _load_model():
    # You can choose 'base', 'small', 'medium', or 'large'
    return whisper.load_model('small')

model = _load_model()

if __name__ == '__main__':
    runpod.serverless.start({'handler': handler})