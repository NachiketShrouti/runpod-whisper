# ─── Dockerfile ───────────────────────────────────────────────────────────────

# 1) Start from slim Python
FROM python:3.10-slim

# 2) Install system deps
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      ffmpeg \
      git \
      python3-dev \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3) Install CPU-only PyTorch
RUN pip3 install --no-cache-dir \
      --index-url https://download.pytorch.org/whl/cpu \
      torch torchvision torchaudio

# 4) Install Whisper (latest) + RunPod SDK
RUN pip3 install --no-cache-dir \
      git+https://github.com/openai/whisper.git \
      runpod

# 5) Copy your handler (with startup/error logging)
COPY handler.py .

# 6) Unbuffered output so logs appear immediately
ENV PYTHONUNBUFFERED=1

# 7) Launch the worker
CMD ["python3", "-u", "handler.py"]
