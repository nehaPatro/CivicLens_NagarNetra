import streamlit as st
from PIL import Image
from io import BytesIO
import requests

# BACKEND URL
BASE_URL = "https://your-backend.onrender.com"   # 🔁 change this after deploy

st.set_page_config(page_title="Civic Lens", layout="wide")

st.title("🚧 Civic Lens")
st.subheader("Smart Urban Issue Detection System")

st.markdown("---")

# Feature selection
feature = st.selectbox(
    "Select Detection Type",
    ["pothole", "flood", "pothole-video", "flood-video"]
)

uploaded_file = st.file_uploader(
    "Upload Image or Video",
    type=["jpg", "jpeg", "png", "mp4"]
)

if uploaded_file:

    col1, col2 = st.columns(2)

    # LEFT → INPUT
    with col1:
        if "video" in uploaded_file.type:
            st.video(uploaded_file)
        else:
            st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)

    # RIGHT → OUTPUT
    with col2:
        if st.button("Detect"):

            with st.spinner("Processing... ⏳"):

                files = {"file": uploaded_file.getvalue()}

                endpoint = f"{BASE_URL}/detect/{feature}"

                response = requests.post(endpoint, files=files)

                if response.status_code == 200:

                    # VIDEO OUTPUT
                    if feature == "pothole-video":
                        st.video(response.content)

                        st.download_button(
                            label="Download Video",
                            data=response.content,
                            file_name="result.mp4",
                            mime="video/mp4"
                        )

                    # IMAGE OUTPUT
                    else:
                        image = Image.open(BytesIO(response.content))

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

                else:
                    st.error("Detection failed ❌")
                    st.write(response.text)

st.markdown("---")
st.success("Upload → Detect → View / Download 🚀")