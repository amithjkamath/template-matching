"""
Inspired by https://www.loginradius.com/blog/engineering/guest-post/opencv-web-app-with-streamlit/
and https://medium.com/analytics-vidhya/finding-waldo-feature-matching-for-opencv-9bded7f5ab10 
"""
import hmac
import numpy as np
import cv2 as cv
import streamlit as st


def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False


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


def main_loop():
    """
    MAIN_LOOP is the main loop (duh) for this streamlit App.
    """
    if not check_password():
        st.stop()

    st.set_page_config(layout="wide")

    st.title("Template Matching Demo")
    st.subheader(
        "This app demonstrates how a template matching algorithm works: by sliding the template across the scene!")

    template_image = cv.imread('waldo-template.jpeg')
    template_image = cv.cvtColor(template_image, cv.COLOR_BGR2RGB)

    st.markdown(
        "To introduce this method, let's first get introduced to our protagonist - Waldo")

    st.text("Introducing Waldo!")
    st.image(template_image, width=100)

    st.markdown(
        "Now for the fun bit - can you find Waldo in the scene below? Most of us will take about 20 seconds, if not more!")

    scene_image = cv.imread("waldo-scene.jpeg")
    scene_image = cv.cvtColor(scene_image, cv.COLOR_BGR2RGB)

    st.text("Can you find Waldo?")
    st.image(scene_image, width=1000)

    st.markdown(
        "Can a computer do better? Certainly. The template matching algorithm is conceptually really simple.")
    st.markdown(
        "The idea is to hold the template over all possible patches in the scene, and then compute a similarity.")
    st.markdown(
        "Naturally, the similarity will be the highest when the template matches what's in the patch underneath.")
    st.markdown(
        "We could then record the location of the maximum similarity, and return it when we have scanned everywhere.")

    corr = compute_correlation(scene_image, template_image)
    norm_corr = (corr - corr.min()) / (corr.max() - corr.min())
    st.text("Here's the correlation image:")
    st.image(norm_corr, width=1000)

    result_image = scene_image.copy()
    threshold = 0.6
    # finding the values where it exceeds the threshold
    loc = np.where(corr >= threshold)
    template_shape = template_image.shape[::-1]  # 3, W, H
    for pt in zip(*loc[::-1]):
        # draw rectangle on places where it exceeds threshold
        cv.rectangle(
            result_image, pt, (pt[0] + template_shape[1], pt[1] + template_shape[2]), (0, 255, 0), 2)

    st.text("Here's the result:")
    st.image(result_image, width=1000)

    st.markdown("How does this work? The template slides across the scene, and \
                 computes the correlation at each location. Use the slider below \
                 to see how this works!")

    alpha = st.slider('Move to slide the template', 0.0,
                      1.0, value=0.00, step=0.0001)
    scene_image = scene_image * 0.25
    scene_image = scene_image.astype(np.uint8)

    norm_corr = cv.copyMakeBorder(norm_corr,
                                  template_shape[2]//2, template_shape[2]//2,
                                  template_shape[1]//2, template_shape[1]//2,
                                  cv.BORDER_CONSTANT)
    norm_corr = cv.multiply(255.0, norm_corr)
    norm_corr = np.dstack((norm_corr, norm_corr, norm_corr))

    out_image = scene_image.copy()
    out_shape = out_image.shape  # H, W, 3
    range_movement = (out_shape[1] - template_shape[1]) * \
        (out_shape[0] - template_shape[2])

    absolute_loc = np.int32(alpha * range_movement)
    absolute_loc_y = absolute_loc // (out_shape[1] - template_shape[1])
    absolute_loc_x = absolute_loc % (out_shape[0] - template_shape[2])
    out_image[0:absolute_loc_y, :, :] = norm_corr[0:absolute_loc_y, :, :]

    out_image[absolute_loc_y:(absolute_loc_y + template_shape[2]),
              absolute_loc_x:(absolute_loc_x + template_shape[1]), :] = template_image

    if absolute_loc_y > (pt[1] + template_shape[2]):
        for pt in zip(*loc[::-1]):
            # draw rectangle on places where it exceeds threshold
            cv.rectangle(
                out_image, pt, (pt[0] + template_shape[1], pt[1] + template_shape[2]), (0, 255, 0), 2)

    st.text("Here's how the correlation is computed:")
    st.image(out_image, width=1000)

    st.markdown("Image copyrights for Where is Waldo - fully attributed to original owners. \
                 It is used here purely for educational purposes.")


if __name__ == '__main__':
    main_loop()
