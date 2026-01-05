#!/bin/bash

# PythonAnywhere Deployment Script
# Run this after uploading to PythonAnywhere

echo "🚀 Setting up Grocery Management System on PythonAnywhere..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3.10 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Initialize database
echo "🗄️ Setting up database..."
python init_db.py

# Load sample data
echo "📊 Loading sample data..."
python sample_data.py

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure WSGI file in PythonAnywhere Web tab"
echo "2. Set up static files mapping"
echo "3. Reload your web app"
echo ""
echo "See DEPLOYMENT.md for detailed instructions"
