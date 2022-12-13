from os.path import exists, join

import streamlit as st
from torch import cuda

from CommentVisualizerLib import CommentVisualizer
from config import ROOT_DIR

def change_images(placeholder, newimage):
    placeholder.empty()
    placeholder.image(newimage)

def main():
    # Paths to stored images
    user_image = join(ROOT_DIR, "image", "user_image.png")
    pre_image = join(ROOT_DIR, "image", "preview_image.png")

    # Title
    st.title("Your comments visualization!")
    placeholder = st.empty()

    if exists(user_image):
        placeholder.image(user_image)
    else:
        placeholder.image(pre_image)

    # Sidebar
    st.sidebar.title('Comment Visualizer')
    st.sidebar.markdown('Visualize your comments!')
    device = st.sidebar.selectbox("Device", ["Cuda", "CPU"]).lower()
    post_link = st.sidebar.text_input('Post link')
    steps = st.sidebar.slider('Steps for processing', min_value=1, max_value=100, value=50)
    height = st.sidebar.slider('Height', min_value=32, max_value=1024, value=512)
    width = st.sidebar.slider('Width', min_value=32, max_value=1024, value=512)
    get_button = st.sidebar.button('Get image')

    # Generate image button
    if get_button:
        try:
            if device == "cuda" and not cuda.is_available():
                raise Exception("Cuda is not available")

            # Initiate neural networks and save them in a session to avoid reinitialization on each request
            with st.spinner("Initializing neural networks..."):
                if "CommentVisualizer" not in st.session_state:
                    st.session_state.CommentVisualizer = CommentVisualizer()

            with st.spinner("Generating image..."):
                image = st.session_state.CommentVisualizer.generate_image(post_url=post_link, device=device, steps=steps, height=height, width=width)
                image.save(f"{user_image}")

            change_images(placeholder, user_image)

        except Exception as e:
            img_name = user_image if exists(user_image) else pre_image
            change_images(placeholder, img_name)
            st.error(str(e))

    # Download image button, exists when a user image is generated
    if exists(user_image):
        with open(user_image, "rb") as fp:
            btn = st.download_button(
                label="Download",
                data=fp,
                file_name=user_image,
            )

if __name__ == "__main__":
    main()
