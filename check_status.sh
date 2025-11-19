#!/bin/bash
# Check status of local repo vs remote repositories

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 Template Matching Demo - Repository Status${NC}"
echo ""

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo -e "${RED}❌ Not a git repository${NC}"
    exit 1
fi

# Get current branch
current_branch=$(git branch --show-current)
echo -e "${BLUE}📍 Current branch:${NC} ${GREEN}${current_branch}${NC}"
echo ""

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    git status --short
    echo ""
else
    echo -e "${GREEN}✅ Working tree clean${NC}"
    echo ""
fi

# Check remotes
echo -e "${BLUE}🔗 Configured remotes:${NC}"
git remote -v | grep "(push)" | while read -r line; do
    echo "  $line"
done
echo ""

# Check sync status with remotes
has_origin=$(git remote | grep -c "^origin$")
has_hf=$(git remote | grep -c "^hf$")

if [ $has_origin -eq 1 ]; then
    echo -e "${BLUE}📦 GitHub (origin):${NC}"
    git fetch origin -q 2>/dev/null
    
    local_commit=$(git rev-parse HEAD)
    origin_commit=$(git rev-parse origin/$current_branch 2>/dev/null)
    
    if [ "$local_commit" = "$origin_commit" ]; then
        echo -e "  ${GREEN}✅ In sync${NC}"
    else
        ahead=$(git rev-list --count origin/$current_branch..HEAD 2>/dev/null || echo "0")
        behind=$(git rev-list --count HEAD..origin/$current_branch 2>/dev/null || echo "0")
        
        if [ "$ahead" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️  Ahead by $ahead commit(s)${NC}"
        fi
        if [ "$behind" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️  Behind by $behind commit(s)${NC}"
        fi
    fi
    echo ""
fi

if [ $has_hf -eq 1 ]; then
    echo -e "${BLUE}🌐 HuggingFace Spaces (hf):${NC}"
    git fetch hf -q 2>/dev/null
    
    local_commit=$(git rev-parse HEAD)
    hf_commit=$(git rev-parse hf/$current_branch 2>/dev/null)
    
    if [ "$local_commit" = "$hf_commit" ]; then
        echo -e "  ${GREEN}✅ In sync${NC}"
    else
        ahead=$(git rev-list --count hf/$current_branch..HEAD 2>/dev/null || echo "0")
        behind=$(git rev-list --count HEAD..hf/$current_branch 2>/dev/null || echo "0")
        
        if [ "$ahead" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️  Ahead by $ahead commit(s)${NC}"
            echo -e "  ${BLUE}💡 Run './deploy.sh' to sync${NC}"
        fi
        if [ "$behind" -gt 0 ]; then
            echo -e "  ${YELLOW}⚠️  Behind by $behind commit(s)${NC}"
        fi
    fi
    echo ""
else
    echo -e "${YELLOW}⚠️  No HuggingFace remote configured${NC}"
    echo -e "${BLUE}💡 To add HuggingFace Spaces remote:${NC}"
    echo -e "   ${GREEN}git remote add hf https://huggingface.co/spaces/amithjkamath/template-matching${NC}"
    echo ""
fi

# Recent commits
echo -e "${BLUE}📝 Recent commits:${NC}"
git log --oneline -5 --decorate
echo ""

# Summary
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Quick Actions:${NC}"
echo "  ./run_local.sh     - Run app locally"
echo "  ./deploy.sh        - Deploy to GitHub & HuggingFace"
echo "  git status         - Check working tree status"
echo "  make help          - See all available commands"
