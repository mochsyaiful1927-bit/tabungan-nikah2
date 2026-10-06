import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="wide")

# CSS Styling Modern, Glassmorphism, & Romantis
st.markdown("""
    <style>
    /* Background Gradient Hangat & Elegan */
    .stApp {
        background: linear-gradient(135deg, #fdfbf7 0%, #f4e8e1 100%);
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
    }

    /* Animasi Love Melayang di Background */
    @keyframes floatLove {
        0% { transform: translateY(0vh) scale(0.6); opacity: 0; }
        50% { opacity: 0.6; }
        100% { transform: translateY(-110vh) scale(1.3); opacity: 0; }
    }
    .floating-hearts {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        overflow: hidden; z-index: 0; pointer-events: none;
    }
    .heart {
        position: absolute; display: block; width: 18px; height: 18px;
        background: rgba(212, 140, 134, 0.25); bottom: -20px;
        animation: floatLove 7s infinite linear; transform: rotate(45deg);
        border-radius: 4px;
    }
    .heart::before, .heart::after {
        content: ''; position: absolute; width: 18px; height: 18px;
        background: rgba(212, 140, 134, 0.25); border-radius: 50%;
    }
    .heart::before { top: -9px; left: 0; }
    .heart::after { left: -9px; top: 0; }
    .heart:nth-child(1) { left: 8%; animation-duration: 6s; animation-delay: 0s; }
    .heart:nth-child(2) { left: 22%; animation-duration: 8s; animation-delay: 2s; }
    .heart:nth-child(3) { left: 38%; animation-duration: 5s; animation-delay: 1s; }
    .heart:nth-child(4) { left: 55%; animation-duration: 9s; animation-delay: 3s; }
    .heart:nth-child(5) { left: 72%; animation-duration: 7s; animation-delay: 1.5s; }
    .heart:nth-child(6) { left: 88%; animation-duration: 6.5s; animation-delay: 4s; }

    .block-container { position: relative; z-index: 1; padding-top: 2rem; }

    /* Sidebar Modern */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(212, 163, 159, 0.2);
    }

    /* Tombol Utama Romantis */
    .stButton>button {
        background: linear-gradient(135deg, #d4a39f 0%, #bc8a86 100%);
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: 600;
        padding: 0.6rem 1rem;
        box-shadow: 0 4px 12px rgba(212, 163, 159, 0.4);
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(188, 138, 134, 0.5);
    }

    /* Kartu Dashboard / Metric Custom Modern */
    [data-testid="metric-container"] {
        background: rgba(255, 255, 255, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(240, 228, 225, 0.8);
        padding: 18px;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.04);
        transition: transform 0.3s ease;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
    }

    /* Header Title Style */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8c6d6b 0%, #5e4644 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0px;
    }
    </style>

    <div class="floating-hearts">
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
    </div>
""", unsafe_allow_html=True)

# Header Modern dengan Emoji Elegan
st.markdown("<h1 class='main-title'>💍 Our Journey to Forever 💍</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a3918f; font-size: 1.1rem; font-weight: 500;'>Tabungan Menuju Halal Fira & Syaiful ✨</p>", unsafe_allow_html=True)
st.markdown("<hr style='border: none; height: 1px; background: linear-gradient(90deg, transparent, #d4a39f, transparent); margin: 25px 0;'>", unsafe_allow_html=True)

# 🔗 LINK WEB APP GOOGLE SCRIPT KAMU
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxbpS8vKgt3cOXfu8pLfP_HWUcRXYejebTRVtVmDsmUb6Q4zwX7a_5HmEo7L1ci5n-o/exec"

# Ambil data dari Google Sheets via API
def load_data():
    try:
        response = requests.get(WEB_APP_URL)
        data = response.json()
        if isinstance(data, list) and len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
    except:
        pass
    return pd.DataFrame(columns=["Tanggal", "Nama", "Jenis", "Jumlah", "Catatan"])

df = load_data()

# Sidebar untuk Input Data
st.sidebar.markdown("<h2 style='color: #8c6d6b; font-weight: 700;'>✨ Tambah Catatan</h2>", unsafe_allow_html=True)
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

# Ringkasan Saldo (Dashboard Modern)
st.markdown("<h3 style='color: #8c6d6b; font-weight: 700; margin-bottom: 20px;'>📊 Ringkasan Keuangan</h3>", unsafe_allow_html=True)

if not df.empty and "Jumlah" in df.columns:
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    
    masuk = df[df["Jenis"] == "Tabungan Masuk"]["Jumlah"].sum()
    keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
    total_saldo = masuk - keluar

    col1, col2, col3 = st.columns(3)
    col1.metric("💖 Total Tabungan", f"Rp {masuk:,.0f}")
    col2.metric("🛍️ Total Keluar", f"Rp {keluar:,.0f}")
    col3.metric("✨ Saldo Bersih", f"Rp {total_saldo:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Tabel Riwayat Transaksi yang Lebih Bersih & Elegan
    st.markdown("<h3 style='color: #8c6d6b; font-weight: 700; margin-bottom: 15px;'>📜 Riwayat Transaksi</h3>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data transaksi atau sedang memuat data...")
