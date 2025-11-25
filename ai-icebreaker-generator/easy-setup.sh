#!/bin/bash

# Easy Setup Script for Non-Developers
# This will ask you questions and set everything up!

clear
echo "=================================="
echo "🎯 AI Icebreaker Generator Setup"
echo "=================================="
echo ""
echo "Welcome! I'll help you set this up step by step."
echo "Don't worry - it's easier than it looks!"
echo ""
echo "Press Enter to continue..."
read

# Step 1: Airtable API Key
clear
echo "=================================="
echo "Step 1: Airtable API Key"
echo "=================================="
echo ""
echo "First, you need your Airtable API key."
echo ""
echo "📋 How to get it:"
echo "1. Go to: https://airtable.com/create/tokens"
echo "2. Click 'Create new token'"
echo "3. Add these scopes: data.records:read and data.records:write"
echo "4. Add access to your base"
echo "5. Copy the token (starts with 'pat')"
echo ""
echo "Do you have your Airtable API key ready?"
echo "(Type 'yes' when ready, or 'help' for more info)"
read READY

if [ "$READY" = "help" ]; then
    echo ""
    echo "Your API key looks like: patAbCdEf123456789..."
    echo "It's like a password that lets this script access your Airtable."
    echo ""
    echo "Press Enter when you have it..."
    read
fi

echo ""
echo "Great! Now paste your Airtable API key here:"
read AIRTABLE_KEY

# Step 2: Base ID
clear
echo "=================================="
echo "Step 2: Airtable Base ID"
echo "=================================="
echo ""
echo "Now you need your Airtable Base ID."
echo ""
echo "📋 How to get it:"
echo "1. Open your Airtable base in your browser"
echo "2. Look at the URL: https://airtable.com/appXXXXXXXXXXXXXX/..."
echo "3. Copy the part that starts with 'app'"
echo ""
echo "Your Base ID looks like: appAbCdEf12345678"
echo ""
echo "Paste your Airtable Base ID here:"
read AIRTABLE_BASE

# Step 3: Table Name
clear
echo "=================================="
echo "Step 3: Table Name"
echo "=================================="
echo ""
echo "What's the name of your table in Airtable?"
echo "(The tab at the bottom - probably 'Leads' or 'Contacts')"
echo ""
echo "Table name:"
read TABLE_NAME

if [ -z "$TABLE_NAME" ]; then
    TABLE_NAME="Leads"
    echo "Using default: Leads"
fi

# Step 4: OpenAI API Key
clear
echo "=================================="
echo "Step 4: OpenAI API Key"
echo "=================================="
echo ""
echo "Finally, you need your OpenAI API key."
echo ""
echo "📋 How to get it:"
echo "1. Go to: https://platform.openai.com/api-keys"
echo "2. Log in (or create an account)"
echo "3. Click 'Create new secret key'"
echo "4. Copy the key (starts with 'sk-')"
echo ""
echo "⚠️  IMPORTANT: Make sure you have credits in your OpenAI account!"
echo "   (Go to Settings > Billing and add $5-10)"
echo ""
echo "Paste your OpenAI API key here:"
read OPENAI_KEY

# Step 5: Verify Airtable Fields
clear
echo "=================================="
echo "Step 5: Check Your Airtable Columns"
echo "=================================="
echo ""
echo "⚠️  IMPORTANT: Your Airtable must have these exact column names:"
echo ""
echo "  ✓ Firstname  (lead's first name)"
echo "  ✓ Company    (company name)"
echo "  ✓ Website    (company website URL)"
echo "  ✓ Role       (their job title - optional)"
echo "  ✓ Icebreaker (leave empty - will be filled automatically)"
echo ""
echo "Do your columns match these names exactly?"
echo "(Type 'yes' to continue, 'no' to see help)"
read COLUMNS_OK

if [ "$COLUMNS_OK" = "no" ]; then
    echo ""
    echo "Please rename your columns in Airtable to match the names above."
    echo "The names must be EXACT (case matters!)."
    echo ""
    echo "After you rename them, run this script again."
    exit 1
fi

# Create .env file
clear
echo "=================================="
echo "Creating Configuration File..."
echo "=================================="
echo ""

cat > .env << EOF
# Airtable Configuration
AIRTABLE_API_KEY=$AIRTABLE_KEY
AIRTABLE_BASE_ID=$AIRTABLE_BASE
AIRTABLE_TABLE_NAME=$TABLE_NAME

# OpenAI Configuration
OPENAI_API_KEY=$OPENAI_KEY

# Processing Configuration
MAX_CONCURRENT=10
ICEBREAKER_FIELD_NAME=Icebreaker
EOF

echo "✅ Configuration saved!"
echo ""

# Install dependencies
echo "=================================="
echo "Installing Dependencies..."
echo "=================================="
echo ""
echo "This might take a minute..."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install
source venv/bin/activate
pip install -q -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""

# Final summary
clear
echo "=================================="
echo "🎉 Setup Complete!"
echo "=================================="
echo ""
echo "Everything is ready to go!"
echo ""
echo "📊 Your configuration:"
echo "  • Airtable Base: $AIRTABLE_BASE"
echo "  • Table Name: $TABLE_NAME"
echo "  • API Keys: ✓ Configured"
echo ""
echo "=================================="
echo "Ready to Generate Icebreakers?"
echo "=================================="
echo ""
echo "Type 'yes' to start now, or 'no' to exit:"
read START_NOW

if [ "$START_NOW" = "yes" ]; then
    echo ""
    echo "Starting the generator..."
    echo ""
    python icebreaker_generator.py
else
    echo ""
    echo "No problem! When you're ready, just run:"
    echo ""
    echo "  cd ai-icebreaker-generator"
    echo "  python icebreaker_generator.py"
    echo ""
    echo "Good luck! 🚀"
fi
