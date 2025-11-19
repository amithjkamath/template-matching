#!/bin/bash
# Alternative simple run script using uv pip directly

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting Template Matching Demo locally...${NC}"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install dependencies if needed
echo -e "${BLUE}📦 Checking dependencies...${NC}"
uv pip install -q -r requirements.txt

# Run the Streamlit app
echo -e "${GREEN}✅ Starting Streamlit app...${NC}"
echo -e "${BLUE}🌐 The app will open at http://localhost:8501${NC}"
echo ""

uv run streamlit run app.py

# If the app exits
echo -e "${BLUE}👋 App stopped.${NC}"