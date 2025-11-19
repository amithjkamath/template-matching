---
title: Template Matching Demo
emoji: 🔍
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
short_description: Interactive demonstration of template matching with Waldo
---

# 🔍 Template Matching Demo

An interactive educational tool that demonstrates how template matching works using computer vision. Learn by doing - click and drag to explore how computers find objects in images!

## 🎯 What is Template Matching?

Template Matching is a simple yet powerful computer vision method that finds the location of a template image within a larger scene by:

1. **Sliding** the template across all possible positions in the scene
2. **Computing** a similarity score at each position
3. **Identifying** the location with the highest similarity score

## 🚀 Try It Live

**[Launch the Interactive Demo](https://huggingface.co/spaces/amithjkamath/template-matching)**

## ✨ Features

- 🖱️ **Interactive Template Placement**: Click anywhere on the image to test template matching
- 📊 **Real-time Correlation Scores**: See quantitative match scores (0.0-1.0) with color coding
- 🔬 **Zoomed Comparison View**: Side-by-side visualization of template vs. current patch
- 🎨 **Educational Heatmaps**: Understand how correlation works across the entire scene
- 🎯 **Instant Feedback**: Learn through exploration and immediate visual feedback

## 💻 Run Locally

### Quick Start

```bash
# Clone the repository
git clone https://github.com/amithjkamath/template-matching.git
cd template-matching

# Run setup (installs uv and dependencies)
./setup.sh

# Run the app
./run_local.sh
```

### Using Make (Alternative)

```bash
make setup    # Initial setup
make run      # Run the app
make deploy   # Deploy to GitHub & HuggingFace
make help     # See all commands
```

### Manual Setup

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --no-build-isolation

# Run the app
uv run --no-build-isolation streamlit run app.py
```

## 📋 Requirements

- Python 3.11 or higher
- [uv](https://github.com/astral-sh/uv) package manager (installed by setup.sh)

## 🛠️ Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development setup and guidelines.

## 📚 What situations could this method be applied to?

Template matching works best when:
- ✅ The template is exactly replicated in the scene
- ✅ Same scale (size) and orientation
- ✅ No rotation or geometric transformations
- ✅ Similar lighting conditions

## ⚠️ When would it not work?

Template matching struggles with:
- ❌ Scale changes (different sizes)
- ❌ Rotation or perspective changes
- ❌ Significant lighting/color differences
- ❌ Partial occlusions

## 🔬 Better Alternatives?

For scenarios with transformations, consider feature-based matching methods:
- **SIFT** (Scale-Invariant Feature Transform)
- **SURF** (Speeded-Up Robust Features)
- **ORB** (Oriented FAST and Rotated BRIEF)
- **AKAZE** (Accelerated-KAZE)

These methods are more robust to scale, rotation, and illumination changes.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎨 Image Attribution

Images from "Where's Waldo?" are copyrighted by their original owners and are used here purely for educational purposes.

## 🙏 Acknowledgments

Inspired by:
- [OpenCV Web App with Streamlit](https://www.loginradius.com/blog/engineering/guest-post/opencv-web-app-with-streamlit/)
- [Finding Waldo: Feature Matching for OpenCV](https://medium.com/analytics-vidhya/finding-waldo-feature-matching-for-opencv-9bded7f5ab10)
