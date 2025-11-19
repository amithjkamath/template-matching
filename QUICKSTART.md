# 🚀 Quick Start Guide

## First Time Setup

1. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
   
   This will:
   - Check Python version (3.11+ required)
   - Install uv package manager if needed
   - Install all dependencies
   - Set script permissions

## Running the App

### Simple Script
If you encounter build issues, use the simpler version:
```bash
./run_simple.sh
```

### Option 3: Make Command
```bash
make run
```

### Option 4: Direct Command
```bash
uv run --no-build-isolation streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deploying to HuggingFace Spaces

### Option 1: Shell Script
```bash
./deploy.sh
```

### Option 2: Make Command
```bash
make deploy
```

The script will:
- Check for uncommitted changes
- Prompt you to commit if needed
- Push to the repository
- HuggingFace Spaces will automatically rebuild

## Troubleshooting

### "Build backend error" or hatchling issues
The project is now configured to skip the build step. If you still see build errors:
```bash
./run_simple.sh
# or
uv pip install -r requirements.txt
uv run streamlit run app.py
```

### "Module not found" error
```bash
uv sync --no-build-isolation
# or
uv pip install -r requirements.txt
```

### Port 8501 already in use
```bash
uv run --no-build-isolation streamlit run app.py --server.port 8502
```

### Script permission denied
```bash
chmod +x setup.sh run_local.sh run_simple.sh deploy.sh
```

## Available Commands

Run `make help` to see all available commands:

```bash
make help        # Show all commands
make setup       # Initial setup
make install     # Install dependencies
make run         # Run locally
make deploy      # Deploy to HuggingFace
make clean       # Clean cache files
make update      # Update dependencies
make info        # Show project info
```

## Need Help?

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed documentation.
