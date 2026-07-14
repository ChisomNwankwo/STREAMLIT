import pandas as pd
import numpy as np
import seaborn as sb
import plotly.express as px
import streamlit as st
import os
import sys
import streamlit.components.v1 as components
import base64
from pathlib import Path

#import scripts
from src import data_loader, processing


st.markdown("""
<style>

/* ===== MAIN APP BACKGROUND ===== */
.stApp {
    background-color: #0b0f1a;
}

/* ===== TEXT ===== */
html, body, [class*="css"] {
    color: #e6e6e6;
    font-family: 'Segoe UI', sans-serif;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: #e6e6e6;
}

/* ===== HEADERS ===== */
h1, h2, h3 {
    color: #ffffff;
    font-weight: 700;
}

/* ===== CARD STYLE ===== */
.card {
    background-color: #1c2433;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.4);
}

/* ===== ACCENT (ESPN RED) ===== */
.accent {
    color: #ff4b4b;
    font-weight: bold;
}

/* ===== BUTTONS ===== */
.stButton>button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton>button:hover {
    background-color: #e03a3a;
    color: white;
}

</style>
""", unsafe_allow_html=True)
#--------------------------------------------------------------------------------------------

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)

#import scripts
from src import data_loader, processing

#set page config
st.set_page_config(layout = 'wide')

#TITLE
st.title("🏀 Interactive NCAA Tournament Dashboard")

#-----------------------------------------------------------------------------------------------------
# ---- Function to convert image to base64 ----
def get_base64(image_path):
    p = Path(image_path)

    st.write("Current directory:", Path.cwd())
    st.write("Trying to open:", p)
    st.write("Absolute path:", p.resolve())
    st.write("Exists?", p.exists())

    if not p.exists():
        st.write("Files in current directory:")
        st.write(list(Path.cwd().iterdir()))

        images = Path.cwd() / "images"
        if images.exists():
            st.write("Files in images folder:")
            st.write(list(images.iterdir()))

        raise FileNotFoundError(f"{p} not found")

    with open(p, "rb") as f:
        return base64.b64encode(f.read()).decode()
        
#def get_base64(image_path):
  #  with open(image_path, "rb") as f:
  #      return base64.b64encode(f.read()).decode()

# ---- Load your images ----
img1 = get_base64("images/1.jpg")
img2 = get_base64("images/2.jpg")
img3 = get_base64("images/3.jpg")
img4 = get_base64("images/4.jpg")
img5 = get_base64("images/5.jpg")
img6 = get_base64("images/6.jpg")
img7 = get_base64("images/7.jpg")
img8 = get_base64("images/8.jpg")


# ---- HTML + CSS + JS ----
html_code = f"""
<!DOCTYPE html>
<html>
<head>
<style>
.slideshow-container {{
  max-width: 1000px;
  position: relative;
  margin: auto;
}}

.mySlides {{
  display: none;
}}

img {{
  width: 100%;
  border-radius: 10px;
}}

.text {{
  color: #fff;
  font-size: 16px;
  position: absolute;
  bottom: 10px;
  width: 100%;
  text-align: center;
}}

.fade {{
  animation: fade 1.5s;
}}

@keyframes fade {{
  from {{opacity: .4}} 
  to {{opacity: 1}}
}}
</style>
</head>

<body>

<div class="slideshow-container">

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img1}">
  </div>

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img2}">
  </div>

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img3}">
  </div>

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img4}">
  </div>

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img5}">
  </div>

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img6}">
  </div>

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img7}">
  </div>

  <div class="mySlides fade">
    <img src="data:image/jpeg;base64,{img8}">
  </div>

</div>

<script>
let slideIndex = 0;
showSlides();

function showSlides() {{
  let i;
  let slides = document.getElementsByClassName("mySlides");

  for (i = 0; i < slides.length; i++) {{
    slides[i].style.display = "none";
  }}

  slideIndex++;
  if (slideIndex > slides.length) {{slideIndex = 1}}

  slides[slideIndex-1].style.display = "block";

  setTimeout(showSlides, 2000);
}}
</script>

</body>
</html>
"""

# ---- Render in Streamlit ----
components.html(html_code, height=500)

st.write('----')

#MEN DATA
@st.cache_data
def get_data():
    return pd.read_csv("https://raw.githubusercontent.com/ChisomNwankwo/ml-datasets/refs/heads/main/processed/mens_team.csv")
    
men_df = get_data()


#WOMEN DATA
@st.cache_data
def get_data_f():
    return pd.read_csv("https://raw.githubusercontent.com/ChisomNwankwo/ml-datasets/refs/heads/main/processed/womens_team.csv") 
    
women_df = get_data_f()


#------------MEN------------
@st.cache_data
def get_men_points():
    return processing.top_5_points(men_df)

@st.cache_data
def get_women_points():
    return processing.top_5_points(women_df)

@st.cache_data
def get_men_rebounds():
    return processing.top_5_rebounds(men_df)

@st.cache_data
def get_women_rebounds():
    return processing.top_W_rebounds(women_df)

@st.cache_data
def get_men_assists():
    return processing.top_5_assists(men_df)

@st.cache_data
def get_women_assists():
    return processing.top_W_assists(women_df)


#----------------------------------------------------------------------------------------------

st.subheader("📊 Quick Stats")
left, right = st.columns(2)

if left.button("Men Basketball", width = 'stretch'):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('**Points**')
        men_points_df = get_men_points()
        st.dataframe(men_points_df, hide_index=True)

    with col2:
        st.markdown('**Assists**')
        men_ast_df = get_men_assists()
        st.dataframe(men_ast_df, hide_index=True)

    
    with col3:
        st.markdown("**Rebounds**")
        men_reb_df = get_men_rebounds()
        st.dataframe(men_reb_df, hide_index=True)


if right.button("Women Basketball", width = 'stretch'):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('**Points**')
        women_pts_df = get_women_points()
        st.dataframe(women_pts_df, hide_index=True)


    with col2:
        st.markdown('**Assists**')
        women_ast_df = get_women_assists()
        st.dataframe(women_ast_df, hide_index=True)

    
    with col3:
        st.markdown("**Rebounds**")
        women_reb_df = get_women_rebounds()
        st.dataframe(women_reb_df, hide_index=True)
