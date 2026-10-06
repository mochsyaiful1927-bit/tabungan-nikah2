import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="centered")

# CSS Styling Background Love Bergerak & Estetik
st.markdown("""
    <style>
    .stApp {
        background-color: #faf7f5;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    @keyframes floatLove {
        0% { transform: translateY(0vh) scale(0.8); opacity: 0; }
        50% { opacity: 0.8; }
        100% { transform: translateY(-100vh) scale(1.2); opacity: 0; }
    }
    .floating-hearts {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        overflow: hidden; z-index: 0; pointer-events: none;
    }
    .heart {
        position: absolute; display: block; width: 20px; height: 20px;
        background: rgba(212, 163, 159, 0.3); bottom: -20px;
        animation: floatLove 8s infinite linear; transform: rotate(45deg);
    }
    .heart::before, .heart::after {
        content: ''; position: absolute; width: 20px; height: 20px;
        background: rgba(212, 163, 159, 0.3); border-radius: 50%;
    }
    .heart::before { top: -10px; left: 0; }
    .heart::after { left: -10px; top: 0; }
    .heart:nth-child(1) { left: 10%; animation-duration: 7s; animation-delay: 0s; }
    .heart:nth-child(2) { left: 25%; animation-duration: 9s; animation-delay: 2s; }
    .heart:nth-child(3) { left: 40%; animation-duration: 6s; animation-delay: 4s; }
    .heart:nth-child(4) { left: 55%; animation-duration: 8s; animation-delay: 1s; }
    .heart:nth-child(5) { left: 70%; animation-duration: 10s; animation-delay: 3s; }
    .heart:nth-child(6) { left: 85%; animation-duration: 7s; animation-delay: 5s; }

    .block-container { position: relative; z-index: 1; }
    [data-testid="stSidebar"] { background-color: #fcf8f7; border-right: 1px solid #f0e4e1; }
    .stButton>button {
        background-color: #d4a39f; color: white; border-radius: 10px;
        border: none; font-weight: bold; width: 100%;
    }
    .stButton>button:hover { background-color: #bc8a86; color: white; }
    </style>

    <div class="floating-hearts">
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
    </div>
""", unsafe_allow_html=True)

# Judul Romantis
st.markdown("<h1 style='text-align: center; color: #8c6d6b;'>💍 Our Journey to Forever 💍</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #b08984; font-weight: normal;'>Tabungan Menuju Halal Fira & Syaiful</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3918f;'>Pantau impian kita bersama secara <i>real-time</i> dari HP atau laptop 💕</p>", unsafe_allow_html=True)
st.markdown("---")

# 🔗 LINK WEB APP GOOGLE SCRIPT KAMU
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxnWs3wKrVlfwAx3Rx4wFA70ysig28hPsyZJ2Dz1GlToJC_RxFHU3umSsmsqT90suiM3g/exec"

# Ambil data dari Google Sheets via API (Tanpa Cache agar data langsung update)
def load_data():
    try:
        response = requests.get(WEB_APP_URL)
        data = response.json()
        if isinstance(data, list) and len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
    return pd.DataFrame(columns=["Tanggal", "Nama", "Jenis", "Jumlah", "Catatan"])

df = load_data()

# Sidebar untuk Input Data
st.sidebar.markdown("<h2 style='color: #8c6d6b;'>✨ Tambah Catatan</h2>", unsafe_allow_html=True)
with st.sidebar.form("form_tabungan", clear_on_submit=True):
    tanggal = st.date_input("Tanggal", datetime.today())
    nama = st.selectbox("Penyetor / Pengambil", ["Syaiful", "Fira", "Bersama"])
    jenis = st.selectbox("Jenis Transaksi", ["Tabungan Masuk", "Pengeluaran"])
    jumlah = st.number_input("Nominal (Rp)", min_value=0, step=50000)
    catatan = st.text_input("Catatan (opsional)", placeholder="cth: Nabung pertama / Beli seserahan")
    
    submit = st.form_submit_button("Simpan Data 💕")
    
    if submit:
        payload = {
            "tanggal": str(tanggal),
            "nama": nama,
            "jenis": jenis,
            "jumlah": jumlah,
            "catatan": catatan
        }
        try:
            requests.post(WEB_APP_URL, json=payload)
            st.sidebar.success("Yeay! Data berhasil disimpan ke Cloud! 🎉")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Gagal menyimpan: {e}")

# Ringkasan Saldo (Dashboard)
st.markdown("<h3 style='color: #8c6d6b;'>📊 Ringkasan Keuangan</h3>", unsafe_allow_html=True)

if not df.empty and "Jumlah" in df.columns:
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    
    masuk = df[df["Jenis"] == "Tabungan Masuk"]["Jumlah"].sum()
    keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
    total_saldo = masuk - keluar

    col1, col2, col3 = st.columns(3)
    col1.metric("💖 Total Tabungan", f"Rp {masuk:,.0f}")
    col2.metric("🛍️️ Total Keluar", f"Rp {keluar:,.0f}")
    col3.metric("✨ Saldo Bersih", f"Rp {total_saldo:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabel Riwayat Transaksi
    st.markdown("<h3 style='color: #8c6d6b;'>📜 Riwayat Transaksi</h3>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data transaksi atau sedang memuat data...")
