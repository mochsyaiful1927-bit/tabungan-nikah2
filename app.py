import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="centered")

# CSS Styling: Background Love Bergerak + Tampilan Modern Finansial
st.markdown("""
    <style>
    .stApp {
        background-color: #fcf8f7;
        font-family: 'Inter', Helvetica, Arial, sans-serif;
    }
    
    /* Efek Animasi Love Melayang di Background */
    @keyframes floatLove {
        0% { transform: translateY(0vh) scale(0.7); opacity: 0; }
        50% { opacity: 0.7; }
        100% { transform: translateY(-110vh) scale(1.3); opacity: 0; }
    }
    .floating-hearts {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        overflow: hidden; z-index: 0; pointer-events: none;
    }
    .heart {
        position: absolute; display: block; width: 20px; height: 20px;
        background: rgba(212, 163, 159, 0.35); bottom: -20px;
        animation: floatLove 7s infinite linear; transform: rotate(45deg);
        border-radius: 4px;
    }
    .heart::before, .heart::after {
        content: ''; position: absolute; width: 20px; height: 20px;
        background: rgba(212, 163, 159, 0.35); border-radius: 50%;
    }
    .heart::before { top: -10px; left: 0; }
    .heart::after { left: -10px; top: 0; }
    .heart:nth-child(1) { left: 10%; animation-duration: 6s; animation-delay: 0s; }
    .heart:nth-child(2) { left: 25%; animation-duration: 8s; animation-delay: 2s; }
    .heart:nth-child(3) { left: 42%; animation-duration: 5s; animation-delay: 1s; }
    .heart:nth-child(4) { left: 60%; animation-duration: 9s; animation-delay: 3s; }
    .heart:nth-child(5) { left: 78%; animation-duration: 6.5s; animation-delay: 1.5s; }
    .heart:nth-child(6) { left: 90%; animation-duration: 7.5s; animation-delay: 4s; }

    /* Supaya konten berada di atas animasi background */
    .block-container { position: relative; z-index: 1; }

    /* Header Banner Impian */
    .banner-card {
        background: linear-gradient(135deg, #d4a39f 0%, #e6ccb2 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(212, 163, 159, 0.2);
        margin-bottom: 20px;
    }
    .banner-title {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
        margin-bottom: 5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }

    /* Card Kartu Putih Modern */
    .modern-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid rgba(240, 228, 225, 0.8);
        margin-bottom: 20px;
    }

    /* Badge Status */
    .badge-on-track {
        background-color: #27ae60;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* Sidebar Clean Style */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-right: 1px solid #f0e4e1;
    }
    .stButton>button {
        background: linear-gradient(135deg, #d4a39f 0%, #bc8a86 100%);
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem;
        box-shadow: 0 4px 10px rgba(212, 163, 159, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #bc8a86 0%, #a37370 100%);
        color: white;
    }
    </style>

    <!-- Elemen Love Melayang di Background -->
    <div class="floating-hearts">
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
    </div>
""", unsafe_allow_html=True)

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

# Hitung Keuangan
if not df.empty and "Jumlah" in df.columns:
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    masuk = df[df["Jenis"] == "Tabungan Masuk"]["Jumlah"].sum()
    keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
    total_saldo = masuk - keluar
else:
    masuk = 0
    keluar = 0
    total_saldo = 0

# Target Nikah (Bisa disesuaikan total target impian kalian, cth: Rp 50.000.000)
TARGET_NIKAH = 50000000 
progress = min(total_saldo / TARGET_NIKAH, 1.0) if TARGET_NIKAH > 0 else 0

# Banner Utama ala Aplikasi Finansial Impian
st.markdown("""
    <div class="banner-card">
        <div style="font-size: 2.5rem; margin-bottom: 5px;">💍👩‍❤️‍👨👰‍♀️</div>
        <div class="banner-title">Nikah Sama Ayang Fira & Syaiful</div>
        <p style="color: #fefefe; font-size: 0.95rem; margin: 0; font-weight: 500;">Menuju lembaran baru yang sakinah, mawaddah, warahmah ✨</p>
    </div>
""", unsafe_allow_html=True)

# Navigasi Tab Modern
tab1, tab2 = st.tabs(["📊 Overview", "📜 Riwayat Transaksi"])

with tab1:
    # Card Status & Progress
    st.markdown("""
        <div class="modern-card" style="text-align: center;">
            <span class="badge-on-track">ON TRACK ✨</span>
            <p style="color: #8c6d6b; margin-bottom: 5px; font-size: 0.9rem; font-weight: 600;">Total Tabungan Terkumpul</p>
            <h1 style="color: #5e4644; font-weight: 800; margin-top: 0;">Rp {:,.0f}</h1>
            <p style="color: #a3918f; font-size: 0.85rem;">dari target Rp {:,.0f}</p>
        </div>
    """.format(total_saldo, TARGET_NIKAH), unsafe_allow_html=True)

    # Progress Bar Interaktif
    st.progress(progress)
    st.caption(f"Pencapaian: **{progress * 100:.1f}%** dari total target impian.")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Rincian Detail Angka
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("💖 Tabungan Masuk", f"Rp {masuk:,.0f}")
    with col_b:
        st.metric("🛍️ Total Keluar", f"Rp {keluar:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Pesan Motivasi Romantis
    st.markdown("""
        <div style="background-color: rgba(255, 255, 255, 0.8); border-left: 5px solid #d4a39f; padding: 15px; border-radius: 10px; backdrop-filter: blur(5px);">
            <p style="margin: 0; color: #8c6d6b; font-weight: 500;">
                💕 <b>Keren! Tabungan kalian on-track nih!</b> Tetap semangat menabung bareng Fira & Syaiful biar impian akad tercapai tepat waktu! 💍✨
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("<h3 style='color: #8c6d6b;'>📜 Riwayat Transaksi</h3>", unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data transaksi yang tercatat.")

# Sidebar untuk Input Data
st.sidebar.markdown("<h2 style='color: #8c6d6b;'>✨ Tambah Catatan</h2>", unsafe_allow_html=True)
with st.sidebar.form("form_tabungan", clear_on_submit=True):
    tanggal = st.date_input("Tanggal", datetime.today())
    nama = st.selectbox("Penyetor / Pengambil", ["Syaiful", "Fira", "Bersama"])
    jenis = st.selectbox("Jenis Transaksi", ["Tabungan Masuk", "Pengeluaran"])
    jumlah = st.number_input("Nominal (Rp)", min_value=0, step=50000)
    catatan = st.text_input("Catatan (opsional)", placeholder="cth: Nabung pertama / Beli seserahan")
    
    submit = st.form_submit_button("Simpan ke Cloud 💕")
    
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
            st.sidebar.success("Yeay! Data berhasil disimpan! 🎉")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Gagal menyimpan: {e}")
