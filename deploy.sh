#!/usr/bin/env bash
set -e

echo "🚀 Deploying XueDao AI Service (existing repo)..."

# ===============================
# CONFIG
# ===============================
APP_DIR="/var/www/xuedao-ai-service"
PYTHON_BIN="/usr/bin/python3.10"
VENV_DIR="$APP_DIR/venv"
BRANCH="main"

cd "$APP_DIR"

# ===============================
# SYSTEM DEPENDENCIES
# ===============================
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y \
  git \
  python3 \
  python3-venv \
  python3-dev \
  build-essential


# ===============================
# GIT UPDATE (NO CLONE)
# ===============================
echo "🔄 Updating existing repository..."
git fetch origin
git checkout "$BRANCH"
git reset --hard "origin/$BRANCH"

# ===============================
# PYTHON VENV
# ===============================
if [ ! -d "$VENV_DIR" ]; then
  echo "🐍 Creating Python 3.11 virtual environment..."
  "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

echo "🐍 Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# ===============================
# PYTHON DEPENDENCIES
# ===============================
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ===============================
# ENV CHECK
# ===============================
if [ ! -f ".env" ]; then
  echo "❌ .env file missing!"
  echo "👉 Create /var/www/xuedao-ai-service/.env before running"
else
  echo "🔐 .env file detected"
fi

# ===============================
# CHROMA DB DIR
# ===============================
if [ ! -d "chroma" ]; then
  echo "🧠 Creating Chroma directory..."
  mkdir chroma
fi

# ===============================
# STOP OLD SERVICES
# ===============================
echo "🛑 Stopping old FastAPI processes..."
pkill -f "uvicorn main:app" || true

# ===============================
# DONE
# ===============================
echo ""
echo "✅ Deployment complete"
echo ""
echo "▶ To start service:"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""

