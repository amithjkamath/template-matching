# CONTRIBUTING.md

## 🛠️ Development Setup

This project uses [uv](https://github.com/astral-sh/uv) for fast, reliable Python package management.

### Prerequisites

- Python 3.11 or higher
- Git

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/amithjkamath/template-matching.git
   cd template-matching
   ```

2. **Run setup**
   ```bash
   ./setup.sh
   ```
   
   Or if you prefer using Make:
   ```bash
   make setup
   ```

3. **Run the app locally**
   ```bash
   ./run_local.sh
   # or
   make run
   ```

### Manual Setup

If you prefer to set things up manually:

1. **Install uv** (if not already installed)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies**
   ```bash
   uv sync --no-build-isolation
   ```

3. **Run the app**
   ```bash
   uv run --no-build-isolation streamlit run app.py
   ```

### Alternative Simple Method

If you encounter build-related issues, you can use a simpler approach:

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the app
uv run streamlit run app.py
```

## 📋 Available Commands

### Using Shell Scripts

- `./setup.sh` - Initial setup (install uv and dependencies)
- `./run_local.sh` - Run the app locally
- `./deploy.sh` - Deploy to HuggingFace Spaces

### Using Makefile

- `make help` - Show all available commands
- `make setup` - Initial setup
- `make install` - Install/update dependencies
- `make run` - Run the app locally
- `make deploy` - Deploy to HuggingFace
- `make clean` - Clean up cache and temporary files
- `make format` - Format code (requires black)
- `make lint` - Run linting checks (requires ruff)
- `make update` - Update all dependencies
- `make info` - Show project information

## 🧪 Testing Locally

Before deploying, always test your changes locally:

1. Run the app: `./run_local.sh`
2. Open your browser to http://localhost:8501
3. Test all interactive features
4. Check console for any errors

## 🚀 Deployment Process

The app is deployed to HuggingFace Spaces. To deploy:

1. **Ensure all changes are committed**
   ```bash
   git status
   git add .
   git commit -m "Your commit message"
   ```

2. **Deploy**
   ```bash
   ./deploy.sh
   # or
   make deploy
   ```

The script will:
- Check for uncommitted changes
- Push to the remote repository
- HuggingFace Spaces will automatically rebuild

## 📦 Dependency Management

### Adding a new dependency

1. **Add to pyproject.toml**
   ```toml
   dependencies = [
       "new-package>=1.0.0",
       ...
   ]
   ```

2. **Update requirements.txt** (for HuggingFace Spaces)
   ```
   new-package>=1.0.0
   ```

3. **Sync dependencies**
   ```bash
   uv sync --no-build-isolation
   # or
   make install
   ```

### Updating dependencies

```bash
uv sync --upgrade --no-build-isolation
# or
make update
```

## 🎨 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### Formatting (optional)

Install formatting tools:
```bash
uv add --dev black ruff
```

Format code:
```bash
make format
```

Lint code:
```bash
make lint
```

## 📝 Making Changes

1. Create a new branch for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Test locally
   ```bash
   make run
   ```

4. Commit your changes
   ```bash
   git add .
   git commit -m "Description of changes"
   ```

5. Push and create a pull request (if working with others)
   ```bash
   git push origin feature/your-feature-name
   ```

6. Or merge to main and deploy
   ```bash
   git checkout main
   git merge feature/your-feature-name
   make deploy
   ```

## 🐛 Troubleshooting

### Module not found error

If you see `ModuleNotFoundError`:
```bash
uv sync --no-build-isolation  # or make install
# Alternative:
uv pip install -r requirements.txt
```

### Build backend errors

The project is configured to skip build steps. If you still encounter hatchling/build errors:
```bash
./run_simple.sh
# or use pip directly:
uv pip install -r requirements.txt
uv run streamlit run app.py
```

### Port already in use

If port 8501 is already in use:
```bash
uv run --no-build-isolation streamlit run app.py --server.port 8502
```

### uv not found

Make sure uv is in your PATH. After installation, restart your terminal or run:
```bash
source ~/.cargo/env
```

## 📚 Project Structure

```
template-matching/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies for HuggingFace Spaces
├── pyproject.toml        # Python project configuration (uv)
├── Dockerfile            # Docker configuration for HF Spaces
├── packages.txt          # System packages for HF Spaces
├── README.md             # User-facing documentation
├── CONTRIBUTING.md       # This file - developer documentation
├── LICENSE               # MIT License
├── setup.sh              # Setup script
├── run_local.sh          # Local run script
├── deploy.sh             # Deployment script
├── Makefile             # Make commands for convenience
└── .gitignore           # Git ignore patterns
```

## 🤝 Contributing Guidelines

1. Keep the educational focus in mind
2. Maintain interactive and engaging features
3. Test thoroughly before deploying
4. Update documentation for any new features
5. Keep dependencies minimal and up-to-date

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
