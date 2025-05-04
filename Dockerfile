# 1) Start from a Python base image with minimal footprint
FROM python:3.10-slim

# 2) Install system and GPU-related dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      ffmpeg \
      git \
      python3-dev \
      build-essential \
      libsndfile1 \
      libglib2.0-0 \
      libsm6 \
      libxrender1 \
      libxext6 \
      wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 3) Install CUDA-enabled PyTorch (let pip auto-detect best version for available GPU)
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 4) Install Whisper (latest) and RunPod SDK
RUN pip install --no-cache-dir \
    git+https://github.com/openai/whisper.git \
    runpod

# 5) Copy handler file
COPY handler.py .

# 6) Enable unbuffered logging
ENV PYTHONUNBUFFERED=1

# 7) Launch the handler
CMD ["python3", "-u", "handler.py"]
