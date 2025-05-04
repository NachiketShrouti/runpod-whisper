# Use an NVIDIA CUDA runtime base so CUDA drivers + libs are pre-installed
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

# Install system dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
      git \
      ffmpeg \
      python3-pip \
      python3-dev \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 1) Install PyTorch for CUDA 11.7
RUN pip3 install --no-cache-dir \
      --index-url https://download.pytorch.org/whl/cu117 \
      torch torchvision torchaudio

# 2) Install Whisper (latest from GitHub) and RunPod SDK
RUN pip3 install --no-cache-dir \
      git+https://github.com/openai/whisper.git \
      runpod

# Copy in your handler
COPY handler.py .

# Ensure unbuffered logs so errors show up immediately
ENV PYTHONUNBUFFERED=1

# Launch the worker
CMD ["python3", "-u", "handler.py"]
