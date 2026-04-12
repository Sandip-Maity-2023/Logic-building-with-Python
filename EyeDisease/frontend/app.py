from pathlib import Path
import sys

import streamlit as st
from PIL import Image


BACKEND_DIR = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from newR import class_names, predict_with_confidence  # noqa: E402


st.set_page_config(page_title="Eye Disease Detection", page_icon="Eye", layout="centered")

st.title("Eye Disease Detection")
st.write("Upload a retinal image to predict the eye disease class using your trained PyTorch model.")

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png"],
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded image", use_container_width=True)

    with st.spinner("Analyzing image..."):
        result = predict_with_confidence(image)

    st.subheader("Prediction")
    st.success(f"{result['label']} ({result['confidence']:.2%} confidence)")

    st.subheader("All class scores")
    for class_name in class_names:
        st.progress(result["probabilities"][class_name], text=f"{class_name}: {result['probabilities'][class_name]:.2%}")
else:
    st.info("Upload an image file to get started.")
