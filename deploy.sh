#!/usr/bin/env bash
set -e

echo "🚀 Deploying XueDao AI Service..."

# ===============================
# CONFIG
# ===============================
APP_DIR="/var/www/xuedao-ai-service"
REPO_URL="https://github.com/drchinp/XueDao_AI_Service.git"
PYTHON_BIN="/usr/bin/python3.11"
VENV_DIR="$APP_DIR/venv"
BRANCH="main"

# ===============================
# SYSTEM PACKAGES
# ===============================
echo "📦 Installing system dependencies..."
sudo apt update
sudo apt install -y \
  git \
  python3.11 \
  python3.11-venv \
  python3.11-dev \
  build-essential

# ===============================
# APP DIRECTORY
# ===============================
if [ ! -d "$APP_DIR" ]; then
  echo "📁 Creating app directory..."
  sudo mkdir -p "$APP_DIR"
  sudo chown -R $USER:$USER "$APP_DIR"
fi

cd "$APP_DIR"

# ===============================
# GIT DEPLOY
# ===============================
if [ ! -d ".git" ]; then
  echo "📦 Cloning repository..."
  git clone "$REPO_URL" .
else
  echo "🔄 Updating repository..."
  git fetch origin
  git checkout "$BRANCH"
  git reset --hard "origin/$BRANCH"
fi

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
# PIP & DEPENDENCIES
# ===============================
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# ===============================
# ENV FILE CHECK
# ===============================
if [ ! -f ".env" ]; then
  echo "⚠️  .env file not found!"
  echo "👉 Create /var/www/xuedao-ai-service/.env before running the service"
else
  echo "🔐 .env file detected"
fi

# ===============================
# CHROMA DIR
# ===============================
if [ ! -d "chroma" ]; then
  echo "🧠 Creating Chroma DB directory..."
  mkdir chroma
fi

# ===============================
# STOP OLD PROCESSES
# ===============================
echo "🛑 Stopping old FastAPI processes..."
pkill -f uvicorn || true
pkill -f python || true

# ===============================
# START SERVICE (MANUAL MODE)
# ===============================
echo "🚀 Starting FastAPI service..."
echo "👉 To run manually:"
echo ""
echo "   source venv/bin/activate"
echo "   uvicorn main:app --host 0.0.0.0 --port 8000"
echo ""
echo "✅ Deployment complete."
