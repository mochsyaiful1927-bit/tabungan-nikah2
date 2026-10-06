import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="centered")

st.title("💍 Tabungan Nikah Fira & Syaiful")
st.markdown("Pantau target dan catatan tabungan bersama secara *real-time* dari HP atau laptop!")

# Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# Ambil data yang ada di Google Sheets (ttl=0 supaya datanya selalu *real-time* terbaru)
try:
    df = conn.read(worksheet="Sheet1", ttl=0)
    df = df.dropna(how="all") # Hapus baris kosong
except Exception as e:
    df = pd.DataFrame(columns=["Tanggal", "Nama", "Jenis", "Jumlah", "Catatan"])

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
        # Format data baru
        new_row = pd.DataFrame([{
            "Tanggal": str(tanggal),
            "Nama": nama,
            "Jenis": jenis,
            "Jumlah": jumlah,
            "Catatan": catatan
        }])
        
        # Gabungkan data lama dan data baru
        updated_df = pd.concat([df, new_row], ignore_index=True)
        
        # Simpan kembali ke Google Sheets
        conn.update(worksheet="Sheet1", data=updated_df)
        st.sidebar.success("Data berhasil disimpan ke Cloud! 🎉")
        st.rerun()

# Ringkasan Saldo (Dashboard)
st.subheader("📊 Ringkasan Keuangan")

if not df.empty and "Jumlah" in df.columns:
    # Pastikan kolom Jumlah berbentuk angka
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="fillna").fillna(0)
    
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
    st.info("Belum ada data transaksi. Silakan input melalui menu di sebelah kiri.")
