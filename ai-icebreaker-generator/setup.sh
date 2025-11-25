#!/bin/bash

echo "🚀 AI Icebreaker Generator Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi
echo "✓ Python 3 found"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi
echo "✓ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env file with your API keys!"
    echo ""
else
    echo "✓ .env file already exists"
    echo ""
fi

echo "================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys:"
echo "   - AIRTABLE_API_KEY"
echo "   - AIRTABLE_BASE_ID"
echo "   - OPENAI_API_KEY"
echo ""
echo "2. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the generator:"
echo "   python icebreaker_generator.py"
echo ""
echo "See README.md for detailed instructions."
echo "================================"
