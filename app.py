import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="centered")

# CSS Styling Modern ala Aplikasi Finansial & Romantis
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f6;
        font-family: 'Inter', Helvetica, Arial, sans-serif;
    }
    
    /* Header Banner Impian */
    .banner-card {
        background: linear-gradient(135deg, #a8ede5 0%, #fed6e3 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .banner-title {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 10px;
    }

    /* Card Kartu Putih Modern */
    .modern-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
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
        background-color: #ffffff;
        border-right: 1px solid #eaeaea;
    }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        width: 100%;
        padding: 0.6rem;
    }
    .stButton>button:hover {
        background-color: #34495e;
        color: white;
    }
    </style>
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

# Target Nikah (Bisa diubah sesuai target total kalian, cth: Rp 50.000.000)
TARGET_NIKAH = 50000000 
progress = min(total_saldo / TARGET_NIKAH, 1.0) if TARGET_NIKAH > 0 else 0

# Banner Utama ala "Rincian Mimpi"
st.markdown("""
    <div class="banner-card">
        <div style="font-size: 3rem; margin-bottom: 5px;">💍👩‍❤️‍👨👰‍♀️</div>
        <div class="banner-title">Nikah Sama Ayang Fira & Syaiful</div>
        <p style="color: #555; font-size: 0.95rem; margin: 0;">Impian kita menuju keluarga sakinah, mawaddah, warahmah ✨</p>
    </div>
""", unsafe_allow_html=True)

# Navigasi Tab Modern
tab1, tab2 = st.tabs(["📊 Overview", "📜 Riwayat Transaksi"])

with tab1:
    # Card Kartu Status & Progress
    st.markdown("""
        <div class="modern-card" style="text-align: center;">
            <span class="badge-on-track">ON TRACK ✨</span>
            <p style="color: gray; margin-bottom: 5px; font-size: 0.9rem;">Total Tabungan Terkumpul</p>
            <h1 style="color: #2c3e50; font-weight: 800; margin-top: 0;">Rp {:,.0f}</h1>
            <p style="color: #888; font-size: 0.85rem;">dari target Rp {:,.0f}</p>
        </div>
    """.format(total_saldo, TARGET_NIKAH), unsafe_allow_html=True)

    # Progress Bar Interaktif
    st.progress(progress)
    st.caption(f"Pencapaian: **{progress * 100:.1f}%** dari total target impian.")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Rincian Detail Angka
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("🟢 Tabungan Masuk", f"Rp {masuk:,.0f}")
    with col_b:
        st.metric("🔴 Total Pengeluaran", f"Rp {keluar:,.0f}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Pesan Motivasi ala Aplikasi
    st.markdown("""
        <div style="background-color: #e8f8f5; border-left: 5px solid #27ae60; padding: 15px; border-radius: 10px;">
            <p style="margin: 0; color: #117a65; font-weight: 500;">
                🔥 <b>Keren! Tabungan kalian on-track nih!</b> Tetap konsisten menabung setiap bulan biar impian akad dan resepsi tercapai tepat waktu! 💍✨
            </p>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📜 Riwayat Transaksi Masuk & Keluar")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data transaksi yang tercatat.")

# Sidebar untuk Input Data
st.sidebar.markdown("<h2 style='color: #2c3e50;'>➕ Tambah Tabungan</h2>", unsafe_allow_html=True)
with st.sidebar.form("form_tabungan", clear_on_submit=True):
    tanggal = st.date_input("Tanggal", datetime.today())
    nama = st.selectbox("Penyetor / Pengambil", ["Syaiful", "Fira", "Bersama"])
    jenis = st.selectbox("Jenis Transaksi", ["Tabungan Masuk", "Pengeluaran"])
    jumlah = st.number_input("Nominal (Rp)", min_value=0, step=50000)
    catatan = st.text_input("Catatan (opsional)", placeholder="cth: Tabungan bulanan / DP Gedung")
    
    submit = st.form_submit_button("Simpan ke Cloud 🚀")
    
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
