#!/bin/bash
# Script to deploy the app to HuggingFace Spaces and GitHub

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Deploying Template Matching Demo...${NC}"
echo ""

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}❌ Not a git repository${NC}"
    exit 1
fi

# Check if there are uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  You have uncommitted changes. Please commit them first.${NC}"
    echo ""
    echo "Uncommitted files:"
    git status --short
    echo ""
    read -p "Do you want to commit all changes now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
        echo -e "${GREEN}✅ Changes committed${NC}"
        echo ""
    else
        echo -e "${RED}❌ Deployment cancelled. Please commit your changes first.${NC}"
        exit 1
    fi
fi

# Get current branch
current_branch=$(git branch --show-current)
echo -e "${BLUE}📍 Current branch: ${current_branch}${NC}"

# Check if we're on main/master branch
if [[ "$current_branch" != "main" && "$current_branch" != "master" ]]; then
    echo -e "${YELLOW}⚠️  Warning: You're not on the main/master branch${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}❌ Deployment cancelled${NC}"
        exit 1
    fi
fi

# Check which remotes exist
has_origin=$(git remote | grep -c "^origin$")
has_hf=$(git remote | grep -c "^hf$")

echo ""
echo -e "${BLUE}📤 Pushing to remote repositories...${NC}"
echo ""

# Push to GitHub (origin)
if [ $has_origin -eq 1 ]; then
    echo -e "${BLUE}→ Pushing to GitHub (origin)...${NC}"
    git push origin $current_branch
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✅ GitHub updated successfully${NC}"
    else
        echo -e "${RED}  ❌ Failed to push to GitHub${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  No 'origin' remote found, skipping GitHub${NC}"
fi

echo ""

# Push to HuggingFace Spaces (hf)
if [ $has_hf -eq 1 ]; then
    echo -e "${BLUE}→ Pushing to HuggingFace Spaces (hf)...${NC}"
    git push hf $current_branch
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✅ HuggingFace Spaces updated successfully${NC}"
    else
        echo -e "${RED}  ❌ Failed to push to HuggingFace Spaces${NC}"
        echo -e "${YELLOW}  💡 Tip: Make sure you have access to the HuggingFace Space${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}⚠️  No 'hf' remote found${NC}"
    echo -e "${BLUE}💡 To add HuggingFace Spaces remote, run:${NC}"
    echo -e "   ${GREEN}git remote add hf https://huggingface.co/spaces/amithjkamath/template-matching${NC}"
fi

# Success message
echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""

if [ $has_origin -eq 1 ]; then
    echo -e "${BLUE}📦 GitHub Repository:${NC}"
    echo -e "   ${GREEN}https://github.com/amithjkamath/template-matching${NC}"
    echo ""
fi

if [ $has_hf -eq 1 ]; then
    echo -e "${BLUE}🌐 HuggingFace Space:${NC}"
    echo -e "   ${GREEN}https://huggingface.co/spaces/amithjkamath/template-matching${NC}"
    echo ""
    echo -e "${YELLOW}💡 Note: It may take a few minutes for the HuggingFace Space to rebuild.${NC}"
fi
