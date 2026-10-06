import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="centered")

st.title("💍 Tabungan Nikah Fira & Syaiful")
st.markdown("Pantau target dan catatan tabungan bersama secara *real-time* dari HP atau laptop!")

# 🔗 MASUKKAN LINK WEB APP GOOGLE SCRIPT KAMU DI SINI:
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxnWs3wKrVlfwAx3Rx4wFA70ysig28hPsyZJ2DzlGTOLjC_RxFHU3umSsmsqT90suiM3g/exec"

# Ambil data dari Google Sheets via API
@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(WEB_APP_URL)
        data = response.json()
        if len(data) > 1:
            df = pd.DataFrame(data[1:], columns=data[0])
            return df
    except:
        pass
    return pd.DataFrame(columns=["Tanggal", "Nama", "Jenis", "Jumlah", "Catatan"])

df = load_data()

# Sidebar untuk Input Data
st.sidebar.header("➕ Tambah Tabungan / Pengeluaran")
with st.sidebar.form("form_tabungan", clear_on_submit=True):
    tanggal = st.date_input("Tanggal", datetime.today())
    nama = st.selectbox("Penyetor / Pengambil", ["Syaiful", "Fira", "Bersama"])
    jenis = st.selectbox("Jenis Transaksi", ["Tabungan Masuk", "Pengeluaran"])
    jumlah = st.number_input("Nominal (Rp)", min_value=0, step=50000)
    catatan = st.text_input("Catatan (opsional)")
    
    submit = st.form_submit_button("Simpan Data")
    
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
            st.sidebar.success("Data berhasil disimpan ke Cloud! 🎉")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Gagal menyimpan: {e}")

# Ringkasan Saldo (Dashboard)
st.subheader("📊 Ringkasan Keuangan")

if not df.empty and "Jumlah" in df.columns:
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    
    masuk = df[df["Jenis"] == "Tabungan Masuk"]["Jumlah"].sum()
    keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
    total_saldo = masuk - keluar

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tabungan", f"Rp {masuk:,.0f}")
    col2.metric("Total Keluar", f"Rp {keluar:,.0f}")
    col3.metric("Saldo Bersih", f"Rp {total_saldo:,.0f}")

    # Tabel Riwayat Transaksi
    st.subheader("📜 Riwayat Transaksi")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data transaksi atau sedang memuat data...")
