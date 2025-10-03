#!/bin/bash

# OpenGW Agentic Analyzer - Development Startup Script
# This script starts both frontend and backend services with cache prevention

echo "🚀 Starting OpenGW Agentic Analyzer Development Environment"
echo "=================================================="

# Function to check if port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "❌ Port $1 is already in use"
        return 1
    else
        echo "✅ Port $1 is available"
        return 0
    fi
}

# Check required ports
echo "🔍 Checking port availability..."
check_port 8000 || exit 1
check_port 5173 || exit 1

# Start backend
echo ""
echo "🐍 Starting Python Backend (Port 8000)..."
cd backend
source .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
export PYTHONDONTWRITEBYTECODE=1  # Prevent Python cache files
export PYTHONUNBUFFERED=1         # Prevent Python output buffering
python main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if kill -0 $BACKEND_PID 2>/dev/null; then
    echo "✅ Backend started successfully (PID: $BACKEND_PID)"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Start frontend
echo ""
echo "🎨 Starting Vue.js Frontend (Port 5173)..."
cd frontend
export NODE_ENV=development
export VITE_API_BASE_URL=http://localhost:8000
export VITE_CACHE_BUSTER=$(date +%s)
npm run dev &
FRONTEND_PID=$!
cd ..

# Wait for frontend to start
echo "⏳ Waiting for frontend to initialize..."
sleep 5

# Check if frontend is running
if kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "✅ Frontend started successfully (PID: $FRONTEND_PID)"
else
    echo "❌ Frontend failed to start"
    kill $BACKEND_PID 2>/dev/null
    exit 1
fi

echo ""
echo "🎉 Development environment is ready!"
echo "=================================================="
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "💡 Cache prevention is enabled for both services"
echo "🛑 Press Ctrl+C to stop all services"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $BACKEND_PID 2>/dev/null && echo "✅ Backend stopped"
    kill $FRONTEND_PID 2>/dev/null && echo "✅ Frontend stopped"
    echo "👋 Goodbye!"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Keep script running
while true; do
    # Check if both processes are still running
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend process died unexpectedly"
        kill $FRONTEND_PID 2>/dev/null
        exit 1
    fi
    
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ Frontend process died unexpectedly"
        kill $BACKEND_PID 2>/dev/null
        exit 1
    fi
    
    sleep 5
done
