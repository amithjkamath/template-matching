"""
Inspired by https://www.loginradius.com/blog/engineering/guest-post/opencv-web-app-with-streamlit/
and https://medium.com/analytics-vidhya/finding-waldo-feature-matching-for-opencv-9bded7f5ab10
"""

import numpy as np
import cv2 as cv
import streamlit as st
from huggingface_hub import hf_hub_download
from streamlit_image_coordinates import streamlit_image_coordinates


@st.cache_data
def compute_correlation(scene: np.array, template: np.array):
    """
    COMPUTE_CORRELATION computes the correlation between the pixels in scene and template
    when the center of template is placed at location (x, y) on the scene. (x, y) is assumed
    to be within bounds of the scene - this function doesn't check for out of bounds.
    """
    gray_scene = cv.cvtColor(scene, cv.COLOR_BGR2GRAY)
    cv.normalize(gray_scene, gray_scene, 0, 255, cv.NORM_MINMAX)

    gray_template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    cv.normalize(gray_template, gray_template, 0, 255, cv.NORM_MINMAX)

    res = cv.matchTemplate(gray_scene, gray_template, cv.TM_CCOEFF_NORMED)
    return res


def compute_patch_correlation(scene_patch: np.array, template: np.array):
    """
    Compute correlation score between a scene patch and template.
    Returns a score between 0 and 1, where 1 is a perfect match.
    """
    # Ensure patches are the same size
    if scene_patch.shape != template.shape:
        return 0.0

    gray_patch = cv.cvtColor(scene_patch, cv.COLOR_BGR2GRAY)
    cv.normalize(gray_patch, gray_patch, 0, 255, cv.NORM_MINMAX)

    gray_template = cv.cvtColor(template, cv.COLOR_BGR2GRAY)
    cv.normalize(gray_template, gray_template, 0, 255, cv.NORM_MINMAX)

    # Use normalized cross-correlation
    result = cv.matchTemplate(gray_patch, gray_template, cv.TM_CCOEFF_NORMED)
    return float(result[0, 0]) if result.size > 0 else 0.0


def extract_patch(scene: np.array, x: int, y: int, template_shape):
    """
    Extract a patch from the scene centered at (x, y) with the same size as the template.
    """
    h, w = template_shape[0], template_shape[1]

    # Calculate patch boundaries
    y_start = max(0, y - h // 2)
    y_end = min(scene.shape[0], y_start + h)
    x_start = max(0, x - w // 2)
    x_end = min(scene.shape[1], x_start + w)

    # Adjust if we hit boundaries
    if y_end - y_start < h:
        y_start = max(0, y_end - h)
    if x_end - x_start < w:
        x_start = max(0, x_end - w)

    patch = scene[y_start:y_end, x_start:x_end]

    # Pad if necessary (edge cases)
    if patch.shape[0] < h or patch.shape[1] < w:
        patch = cv.copyMakeBorder(
            patch,
            0,
            h - patch.shape[0],
            0,
            w - patch.shape[1],
            cv.BORDER_CONSTANT,
            value=[0, 0, 0],
        )

    return patch, (x_start, y_start, x_end, y_end)


@st.cache_resource
def load_images():
    """Load and cache the template and scene images."""
    # Load template
    template_path = hf_hub_download(
        repo_id="amithjkamath/exampleimages",
        filename="waldo-template.jpeg",
        repo_type="dataset",
    )
    template_image = cv.imread(template_path)
    template_image = cv.cvtColor(template_image, cv.COLOR_BGR2RGB)

    # Load scene
    scene_path = hf_hub_download(
        repo_id="amithjkamath/exampleimages",
        filename="waldo-scene.jpeg",
        repo_type="dataset",
    )
    scene_image = cv.imread(scene_path)
    scene_image = cv.cvtColor(scene_image, cv.COLOR_BGR2RGB)

    return template_image, scene_image


def main_loop():
    """
    MAIN_LOOP is the main loop (duh) for this streamlit App.
    """
    st.set_page_config(layout="wide")

    st.title("🔍 Interactive Template Matching Demo")
    st.markdown(
        """
    Welcome! This app teaches you how **template matching** works - a fundamental computer vision technique.
    You'll learn by doing: click and drag the template around to see how computers "find" objects in images!
    """
    )

    # Load images (cached)
    template_image, scene_image = load_images()

    # Introduction
    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown("### Meet Waldo 👋")
        st.image(template_image, caption="Our template to find")
        st.markdown(
            "**Template size:** {}×{}".format(
                template_image.shape[1], template_image.shape[0]
            )
        )

    with col2:
        st.markdown("### The Challenge")
        st.markdown(
            """
        Can you spot Waldo in this busy scene? Most people take 20+ seconds!
        
        But computers can do it differently. Instead of using intuition, they use **template matching**:
        - Slide the template over every possible position
        - At each position, compute a **similarity score**
        - The highest score reveals where Waldo is!
        """
        )

    # Show the scene
    st.markdown("---")
    st.markdown("### 🎯 Try It Yourself: Interactive Template Matching")
    st.markdown(
        """
    **Instructions:** Click anywhere on the image below to place the template there. 
    Watch how the correlation score changes! Can you find where Waldo actually is?
    """
    )

    # Initialize session state for template position
    if "template_x" not in st.session_state:
        st.session_state.template_x = scene_image.shape[1] // 4
        st.session_state.template_y = scene_image.shape[0] // 4

    if "last_computed_x" not in st.session_state:
        st.session_state.last_computed_x = st.session_state.template_x
        st.session_state.last_computed_y = st.session_state.template_y

    if "computed_score" not in st.session_state:
        st.session_state.computed_score = None

    if "computed_patch" not in st.session_state:
        st.session_state.computed_patch = None

    # Create interactive image
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("**Click on the image to move the template:**")

        # Create overlay image with template
        display_image = scene_image.copy()
        t_h, t_w = template_image.shape[0], template_image.shape[1]

        # Calculate template position (top-left corner)
        x = st.session_state.template_x
        y = st.session_state.template_y
        x_start = max(0, x - t_w // 2)
        y_start = max(0, y - t_h // 2)
        x_end = min(scene_image.shape[1], x_start + t_w)
        y_end = min(scene_image.shape[0], y_start + t_h)

        # Draw rectangle around template position
        cv.rectangle(
            display_image, (x_start, y_start), (x_end, y_end), (255, 255, 0), 3
        )

        # Overlay semi-transparent template
        overlay = display_image.copy()
        if y_end - y_start == t_h and x_end - x_start == t_w:
            overlay[y_start:y_end, x_start:x_end] = cv.addWeighted(
                overlay[y_start:y_end, x_start:x_end], 0.5, template_image, 0.5, 0
            )
            display_image = cv.addWeighted(display_image, 0.7, overlay, 0.3, 0)

        # Get click coordinates
        value = streamlit_image_coordinates(display_image, key="scene_image")

        # Update position only if clicked (value changed)
        if value is not None:
            new_x = value["x"]
            new_y = value["y"]
            # Only update if position actually changed
            if (
                new_x != st.session_state.template_x
                or new_y != st.session_state.template_y
            ):
                st.session_state.template_x = new_x
                st.session_state.template_y = new_y

    with col_right:
        # Show current position
        st.markdown("### 📍 Current Position")
        st.markdown(f"**X:** {st.session_state.template_x}px")
        st.markdown(f"**Y:** {st.session_state.template_y}px")

        # Check if position has changed since last computation
        position_changed = (
            st.session_state.template_x != st.session_state.last_computed_x
            or st.session_state.template_y != st.session_state.last_computed_y
        )

        # Button to compute match
        if position_changed:
            st.info("🔄 Position changed! Click below to compute match score.")

        compute_button = st.button(
            "🔍 Compute Match Score", type="primary", use_container_width=True
        )  # Will be updated to width='stretch' in future

        # Compute correlation if button clicked or initial load
        if compute_button or st.session_state.computed_score is None:
            with st.spinner("Computing correlation..."):
                # Extract patch and compute correlation
                patch, _ = extract_patch(
                    scene_image,
                    st.session_state.template_x,
                    st.session_state.template_y,
                    template_image.shape[:2],
                )

                score = compute_patch_correlation(patch, template_image)

                # Store computed values
                st.session_state.computed_score = score
                st.session_state.computed_patch = patch
                st.session_state.last_computed_x = st.session_state.template_x
                st.session_state.last_computed_y = st.session_state.template_y

        # Display match score with color coding
        st.markdown("### 📊 Match Score")

        if st.session_state.computed_score is not None:
            score = st.session_state.computed_score

            # Determine match quality
            if score >= 0.8:
                quality = "🎉 Excellent Match!"
                color = "green"
                explanation = "This is very likely the correct location!"
            elif score >= 0.6:
                quality = "✅ Good Match"
                color = "blue"
                explanation = "Strong similarity, but maybe not perfect."
            elif score >= 0.4:
                quality = "⚠️ Moderate Match"
                color = "orange"
                explanation = "Some similarity, but probably not the right spot."
            else:
                quality = "❌ Poor Match"
                color = "red"
                explanation = "Very low similarity - keep searching!"

            # Display score with highlighting
            st.markdown(
                f"""
            <div style="background-color: {color}; padding: 20px; border-radius: 10px; text-align: center;">
                <h2 style="color: white; margin: 0;">{score:.3f}</h2>
                <p style="color: white; margin: 5px 0 0 0; font-size: 18px;"><b>{quality}</b></p>
            </div>
            """,
                unsafe_allow_html=True,
            )

            st.markdown(f"*{explanation}*")
        else:
            st.warning("Click 'Compute Match Score' to analyze this position.")

        # Show zoomed comparison
        st.markdown("### 🔬 Close-up Comparison")

        if st.session_state.computed_patch is not None:
            st.markdown("**Template vs Current Patch:**")

            # Create side-by-side comparison
            comparison = np.hstack([template_image, st.session_state.computed_patch])
            st.image(
                comparison,
                caption="Left: Template | Right: Current patch",
                width="stretch",
            )
        else:
            st.info("Compute match score to see the comparison.")

    # Educational section: Show the full correlation heatmap
    st.markdown("---")
    st.markdown("### 🧠 How Does the Computer Find Waldo?")

    with st.expander("Click here to see the full solution!", expanded=False):
        st.markdown(
            """
        The computer doesn't guess - it's systematic! It computes the correlation score at **every possible position**.
        Here's the resulting **correlation heatmap** where brighter areas indicate better matches:
        """
        )

        corr = compute_correlation(scene_image, template_image)
        norm_corr = (corr - corr.min()) / (corr.max() - corr.min())

        col1, col2 = st.columns(2)

        with col1:
            st.image(
                norm_corr,
                caption="Correlation Heatmap (bright = high match)",
                width="stretch",
            )
            st.markdown("Notice the bright spot? That's where Waldo is! 🎯")

        with col2:
            # Show result with bounding boxes
            result_image = scene_image.copy()
            threshold = 0.6
            loc = np.where(corr >= threshold)
            template_shape = template_image.shape

            for pt in zip(*loc[::-1]):
                cv.rectangle(
                    result_image,
                    pt,
                    (pt[0] + template_shape[1], pt[1] + template_shape[0]),
                    (0, 255, 0),
                    3,
                )

            st.image(
                result_image,
                caption="Detected locations (green boxes)",
                width="stretch",
            )
            st.markdown("Green boxes show all locations with correlation > 0.6")

        st.markdown(
            """
        **Key Insight:** Template matching is a brute-force approach that checks every possible location.
        While simple, it's very effective for finding exact or near-exact matches!
        """
        )

    # Footer
    st.markdown("---")
    st.markdown(
        """
    <small>
    🎨 Image copyrights for "Where's Waldo?" are fully attributed to original owners.  
    Used here purely for educational purposes.
    </small>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main_loop()
