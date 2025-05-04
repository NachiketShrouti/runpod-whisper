# Use an NVIDIA runtime base so CUDA is available for GPU-accelerated Whisper
FROM nvidia/cuda:11.7.1-cudnn8-runtime-ubuntu22.04

# Install system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      ffmpeg \
      git \
      python3-pip \
      && rm -rf /var/lib/apt/lists/*

# Install Python deps
# 1) PyTorch CUDA build
# 2) Whisper from GitHub (ensures latest version)
# 3) runpod SDK
RUN pip3 install --no-cache-dir \
      torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117 \
      git+https://github.com/openai/whisper.git \
      runpod

# Copy handler
WORKDIR /app
COPY handler.py .

# Make sure any startup errors get printed
ENV PYTHONUNBUFFERED=1

# Launch
CMD ["python3", "-u", "handler.py"]
