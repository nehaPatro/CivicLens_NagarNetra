import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# ---------------- BACKEND URL ----------------

BASE_URL = "https://civic-lens-backend.onrender.com"

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="Civic Lens",
    layout="wide"
)

# ---------------- TITLE ----------------

st.title("🚧 Civic Lens")

st.subheader("Smart Urban Issue Detection System")

st.markdown("---")

st.markdown("## Welcome")

st.write(
    "Login with Google to continue to the detection dashboard."
)

login_url = f"{BASE_URL}/login"

st.link_button(
    "🔐 Continue with Google",
    login_url
)

st.markdown("---")

# ---------------- DETECTION OPTIONS ----------------

feature = st.selectbox(
    "Select Detection Type",
    [
        "pothole",
        "flood",
        "pothole-video",
        "flood-video"
    ]
)

# ---------------- FILE UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Upload Image or Video",
    type=["jpg", "jpeg", "png", "mp4"]
)

# ---------------- PROCESS ----------------

if uploaded_file:

    col1, col2 = st.columns(2)

    # ---------------- INPUT ----------------

    with col1:

        if "video" in uploaded_file.type:
            st.video(uploaded_file)

        else:
            st.image(
                uploaded_file,
                caption="Uploaded Image",
                use_container_width=True
            )

    # ---------------- OUTPUT ----------------

    with col2:

        if st.button("Detect"):

            with st.spinner("Processing... ⏳"):

                files = {
                    "file": uploaded_file.getvalue()
                }

                endpoint = f"{BASE_URL}/detect/{feature}"

                response = requests.post(
                    endpoint,
                    files=files
                )

                # ---------------- SUCCESS ----------------

                if response.status_code == 200:

                    # -------- VIDEO OUTPUT --------

                    if feature in ["pothole-video", "flood-video"]:

                        st.video(response.content)

                        st.download_button(
                            label="Download Video",
                            data=response.content,
                            file_name="result.mp4",
                            mime="video/mp4"
                        )

                    # -------- IMAGE OUTPUT --------

                    else:

                        image = Image.open(
                            BytesIO(response.content)
                        )

                        st.image(
                            image,
                            caption="Detected Output",
                            use_container_width=True
                        )

                        st.download_button(
                            label="Download Image",
                            data=response.content,
                            file_name="result.jpg",
                            mime="image/jpeg"
                        )

                    st.success("Detection completed 🚀")

                # ---------------- ERROR ----------------

                else:

                    st.error("Detection failed ❌")

                    st.write(response.text)

# ---------------- FOOTER ----------------

st.markdown("---")

st.success("Upload → Detect → View / Download 🚀")