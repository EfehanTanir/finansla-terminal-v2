#!/bin/bash
# FINANSAL TERMINAL - Start Script
# Launches FastAPI backend + Streamlit frontend together

set -e

echo "============================================"
echo "  FINANSAL TERMINAL v2.0 STARTING..."
echo "============================================"

export API_PORT=${API_PORT:-8000}
export STREAMLIT_PORT=${STREAMLIT_PORT:-8501}
export API_URL=${API_URL:-http://localhost:$API_PORT}

echo "[1/2] Starting FastAPI backend on port $API_PORT..."
cd /app
uvicorn backend.main:app --host 0.0.0.0 --port $API_PORT --workers 2 &
BACKEND_PID=$!

echo "[   ] Waiting for backend to be ready..."
sleep 4

echo "[2/2] Starting Streamlit frontend on port $STREAMLIT_PORT..."
streamlit run frontend/app.py \
    --server.port $STREAMLIT_PORT \
    --server.address 0.0.0.0 \
    --server.headless true \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --browser.gatherUsageStats false \
    &
FRONTEND_PID=$!

echo "============================================"
echo "  BACKEND  → http://localhost:$API_PORT"
echo "  FRONTEND → http://localhost:$STREAMLIT_PORT"
echo "============================================"

# Wait for either process to exit
wait -n $BACKEND_PID $FRONTEND_PID

# If one exits, kill the other
kill $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
