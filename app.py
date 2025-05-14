import streamlit as st
import cv2
import pandas as pd
import numpy as np
from PIL import Image

# Load color dataset
@st.cache_data
def load_colors():
    colors = pd.read_csv("colors.csv")
    return colors

colors_df = load_colors()

# Find closest color
def get_closest_color(R, G, B):
    minimum = float('inf')
    cname = ""
    for _, row in colors_df.iterrows():
        d = abs(R - row['R']) + abs(G - row['G']) + abs(B - row['B'])
        if d < minimum:
            minimum = d
            cname = row['color_name']
            match_rgb = (row['R'], row['G'], row['B'])
    return cname, match_rgb

# Streamlit UI
st.title("🎨 Color Detection from Images")
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    image_np = np.array(image)
    
    st.info("Click on the image to detect color (use coordinates)")
    x = st.number_input("X Coordinate", min_value=0, max_value=image_np.shape[1]-1)
    y = st.number_input("Y Coordinate", min_value=0, max_value=image_np.shape[0]-1)
    
    if st.button("Detect Color"):
        b, g, r = image_np[int(y), int(x)]
        color_name, (cr, cg, cb) = get_closest_color(r, g, b)
        
        st.markdown(f"**Detected Color Name:** {color_name}")
        st.markdown(f"**RGB Values:** ({r}, {g}, {b})")
        st.markdown("**Detected Color Preview:**")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({r},{g},{b});border:1px solid #000'></div>",
            unsafe_allow_html=True
        )
