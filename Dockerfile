# Use a slim Python image
FROM python:3.10-slim

# Install ffmpeg for audio processing
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /

# Install Python dependencies
RUN pip install --no-cache-dir runpod whisper

# Copy handler
COPY handler.py /

# Start the Worker
CMD ["python3", "-u", "handler.py"]