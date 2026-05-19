import streamlit as st

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


st.sidebar.info("Still in works...you are welcome to add your code too!")

st.sidebar.subheader("Task")


