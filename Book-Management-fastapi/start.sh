#!/bin/bash
# Quick start script for Book Management API

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate

# Check if MongoDB is running
echo "Checking MongoDB connection..."
if ! mongosh --eval "db.version()" > /dev/null 2>&1; then
    echo "⚠️  Warning: MongoDB doesn't seem to be running!"
    echo "Please start MongoDB before running the application."
    echo ""
    echo "To start MongoDB:"
    echo "  - On Windows: net start MongoDB"
    echo "  - Or run: mongod"
    exit 1
fi

echo "✓ MongoDB is running"

# Start the application
echo ""
echo "Starting Book Management API..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

cd app
python main.py
