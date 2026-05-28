FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Docker cache layer)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create __init__ files if missing
RUN touch frontend/__init__.py \
         frontend/pages/__init__.py \
         frontend/components/__init__.py \
         backend/__init__.py

# Make start script executable
RUN chmod +x start.sh

# Expose ports
EXPOSE 8000 8501

# Default env vars
ENV API_PORT=8000
ENV STREAMLIT_PORT=8501
ENV API_URL=http://localhost:8000
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start both services
CMD ["./start.sh"]
