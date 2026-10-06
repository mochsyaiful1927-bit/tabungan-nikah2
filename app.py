import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="centered")

# CSS Styling Tambahan agar Romantis & Estetik
st.markdown("""
    <style>
    .stApp {
        background-color: #faf7f5;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    [data-testid="stSidebar"] {
        background-color: #fcf8f7;
        border-right: 1px solid #f0e4e1;
    }
    .stButton>button {
        background-color: #d4a39f;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #bc8a86;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Animasi Dino Kuning & Judul Romantis
col_dino1, col_title, col_dino2 = st.columns([1, 4, 1])

with col_dino1:
    # GIF Dino Kuning Lucu (Bergerak)
    st.markdown("<img src='https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif' width='100'>", unsafe_allow_html=True)

with col_title:
    st.markdown("<h1 style='text-align: center; color: #8c6d6b; margin-bottom: 0;'>💍 Our Journey to Forever 💍</h1>", unsafe_allow_html=True)

with col_dino2:
    st.markdown("<img src='https://media.giphy.com/media/LmNwrBhejkK9EFP504/giphy.gif' width='100'>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #b08984; font-weight: normal; margin-top: 0;'>Tabungan Menuju Halal Fira & Syaiful</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3918f;'>Pantau impian kita bersama secara <i>real-time</i> dari HP atau laptop 💕</p>", unsafe_allow_html=True)
st.markdown("---")

# 🔗 LINK WEB APP GOOGLE SCRIPT KAMU
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxnWs3wKrVlfwAx3Rx4wFA70ysig28hPsyZJ2Dz1GlToJC_RxFHU3umSsmsqT90suiM3g/exec"

# Ambil data dari Google Sheets via API
@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(WEB_APP_URL)
        data = response.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
