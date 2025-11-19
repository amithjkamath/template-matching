#!/bin/bash
# Setup script for Template Matching Demo

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 Setting up Template Matching Demo...${NC}"
echo ""

# Check Python version
echo -e "${BLUE}🐍 Checking Python version...${NC}"
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.11.9"

if python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo -e "${GREEN}✅ Python ${python_version} is installed${NC}"
else
    echo -e "${RED}❌ Python 3.11+ is required${NC}"
    exit 1
fi

# Check if uv is installed
echo -e "${BLUE}📦 Checking for uv package manager...${NC}"
if ! command -v uv &> /dev/null; then
    echo -e "${YELLOW}⚠️  uv is not installed${NC}"
    echo -e "${BLUE}Installing uv...${NC}"
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Source the shell configuration to make uv available
    if [ -f "$HOME/.cargo/env" ]; then
        source "$HOME/.cargo/env"
    fi
    
    if command -v uv &> /dev/null; then
        echo -e "${GREEN}✅ uv installed successfully${NC}"
    else
        echo -e "${RED}❌ Failed to install uv. Please install manually:${NC}"
        echo "   curl -LsSf https://astral.sh/uv/install.sh | sh"
        exit 1
    fi
else
    echo -e "${GREEN}✅ uv is already installed${NC}"
fi

# Sync dependencies
echo ""
echo -e "${BLUE}📥 Installing dependencies...${NC}"
uv sync --no-build-isolation

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed successfully${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Make scripts executable
echo ""
echo -e "${BLUE}🔐 Setting script permissions...${NC}"
chmod +x run_local.sh deploy.sh setup.sh

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo -e "${BLUE}Next steps:${NC}"
echo "  1. Run locally:  ${GREEN}./run_local.sh${NC}"
echo "  2. Deploy:       ${GREEN}./deploy.sh${NC}"
echo ""
echo -e "${YELLOW}💡 Tip: You can also use 'make run' or 'make deploy' if you prefer${NC}"
