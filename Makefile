# Makefile for Template Matching Demo
.PHONY: help setup run deploy clean test format lint install status

# Default target
.DEFAULT_GOAL := help

# Colors
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m

help: ## Show this help message
	@echo "$(BLUE)Template Matching Demo - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

setup: ## Initial setup - install uv and dependencies
	@echo "$(BLUE)🔧 Running setup...$(NC)"
	@chmod +x setup.sh
	@./setup.sh

install: ## Install/update dependencies using uv
	@echo "$(BLUE)📦 Installing dependencies...$(NC)"
	@uv sync --no-build-isolation
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

run: ## Run the app locally
	@chmod +x run_local.sh
	@./run_local.sh

deploy: ## Deploy to GitHub & HuggingFace Spaces
	@chmod +x deploy.sh
	@./deploy.sh

status: ## Check repository sync status
	@chmod +x check_status.sh
	@./check_status.sh

clean: ## Clean up cache and temporary files
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name "*.pyo" -delete 2>/dev/null || true
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

format: ## Format code with black and isort (if installed)
	@echo "$(BLUE)🎨 Formatting code...$(NC)"
	@if command -v black > /dev/null; then \
		uv run black app.py; \
	else \
		echo "$(YELLOW)⚠️  black not installed, skipping$(NC)"; \
	fi

lint: ## Run linting checks
	@echo "$(BLUE)🔍 Running linting...$(NC)"
	@if command -v ruff > /dev/null; then \
		uv run ruff check app.py; \
	else \
		echo "$(YELLOW)⚠️  ruff not installed, skipping$(NC)"; \
	fi

test: ## Run tests (if any)
	@echo "$(BLUE)🧪 Running tests...$(NC)"
	@echo "$(YELLOW)⚠️  No tests configured yet$(NC)"

check: format lint ## Run all checks (format + lint)
	@echo "$(GREEN)✅ All checks complete$(NC)"

update: ## Update all dependencies
	@echo "$(BLUE)⬆️  Updating dependencies...$(NC)"
	@uv sync --upgrade --no-build-isolation
	@echo "$(GREEN)✅ Dependencies updated$(NC)"

info: ## Show project information
	@echo "$(BLUE)📊 Project Information$(NC)"
	@echo ""
	@echo "  Name:        Template Matching Demo"
	@echo "  Python:      $$(python3 --version | awk '{print $$2}')"
	@echo "  UV:          $$(uv --version 2>/dev/null || echo 'not installed')"
	@echo "  Repository:  https://github.com/amithjkamath/template-matching"
	@echo "  HF Space:    https://huggingface.co/spaces/amithjkamath/template-matching"
	@echo ""
