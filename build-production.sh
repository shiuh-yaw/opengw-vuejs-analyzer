#!/bin/bash

# OpenGW Agentic Analyzer - Production Build Script
# This script builds the application with comprehensive cache prevention

echo "🏗️  Building OpenGW Agentic Analyzer for Production"
echo "=================================================="

# Set build timestamp
BUILD_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
BUILD_HASH=$(date +%s | sha256sum | head -c 8)

echo "📅 Build Time: $BUILD_TIME"
echo "🔑 Build Hash: $BUILD_HASH"

# Clean previous builds
echo ""
echo "🧹 Cleaning previous builds..."
rm -rf frontend/dist
rm -rf backend/__pycache__
rm -rf backend/**/__pycache__

# Build frontend
echo ""
echo "🎨 Building Vue.js Frontend..."
cd frontend

# Set environment variables for cache busting
export VITE_BUILD_TIME="$BUILD_TIME"
export VITE_BUILD_HASH="$BUILD_HASH"
export VITE_CACHE_BUSTER=$(date +%s)

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Build the application
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Frontend build completed successfully"
else
    echo "❌ Frontend build failed"
    exit 1
fi

cd ..

# Prepare backend
echo ""
echo "🐍 Preparing Python Backend..."
cd backend

# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "📝 Creating requirements.txt..."
    pip freeze > requirements.txt
fi

# Remove Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

echo "✅ Backend preparation completed"

cd ..

# Create deployment package
echo ""
echo "📦 Creating deployment package..."
PACKAGE_NAME="opengw-analyzer-${BUILD_HASH}.tar.gz"

tar -czf "$PACKAGE_NAME" \
    --exclude="frontend/node_modules" \
    --exclude="backend/.venv" \
    --exclude="backend/__pycache__" \
    --exclude=".git" \
    frontend/dist \
    backend/ \
    start-dev.sh \
    README.md

if [ -f "$PACKAGE_NAME" ]; then
    echo "✅ Deployment package created: $PACKAGE_NAME"
    echo "📊 Package size: $(du -h $PACKAGE_NAME | cut -f1)"
else
    echo "❌ Failed to create deployment package"
    exit 1
fi

# Create deployment info
echo ""
echo "📋 Creating deployment information..."
cat > deployment-info.json << EOF
{
  "build_time": "$BUILD_TIME",
  "build_hash": "$BUILD_HASH",
  "package_name": "$PACKAGE_NAME",
  "frontend_dist": "frontend/dist",
  "backend_main": "backend/main.py",
  "cache_prevention": {
    "frontend": {
      "vite_hash_assets": true,
      "meta_cache_control": true,
      "build_time_injection": true
    },
    "backend": {
      "response_headers": true,
      "etag_generation": true,
      "no_python_cache": true
    }
  },
  "deployment_commands": {
    "extract": "tar -xzf $PACKAGE_NAME",
    "backend_start": "cd backend && python main.py",
    "frontend_serve": "Serve frontend/dist with web server"
  }
}
EOF

echo "✅ Deployment info created: deployment-info.json"

echo ""
echo "🎉 Production build completed successfully!"
echo "=================================================="
echo "📦 Package: $PACKAGE_NAME"
echo "📋 Info: deployment-info.json"
echo "🚀 Ready for deployment!"
echo ""
echo "💡 Cache prevention features included:"
echo "   - Asset hash-based naming"
echo "   - HTTP cache control headers"
echo "   - Build-time injection"
echo "   - Python cache disabled"
