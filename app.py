import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman Web
st.set_page_config(page_title="Tabungan Nikah Fira & Syaiful", page_icon="💍", layout="centered")

st.title("💍 Tabungan Nikah Fira & Syaiful")
st.markdown("Pantau target dan catatan tabungan bersama secara *real-time* dari HP atau laptop!")

# Simulasi penyimpanan data sementara
if 'data_tabungan' not in st.session_state:
    st.session_state.data_tabungan = pd.DataFrame(columns=["Tanggal", "Nama", "Jenis", "Jumlah (Rp)", "Catatan"])

# Sidebar untuk Input Data
st.sidebar.header("➕ Tambah Tabungan / Pengeluaran")
with st.sidebar.form("form_tabungan"):
    tanggal = st.date_input("Tanggal", datetime.today())
    nama = st.selectbox("Penyetor / Pengambil", ["Syaiful", "Fira", "Bersama"])
    jenis = st.selectbox("Jenis Transaksi", ["Tabungan Masuk", "Pengeluaran"])
    jumlah = st.number_input("Nominal (Rp)", min_value=0, step=50000)
    catatan = st.text_input("Catatan (opsional)")
    
    submit = st.form_submit_button("Simpan Data")
    
    if submit:
        new_data = {
            "Tanggal": str(tanggal),
            "Nama": nama,
            "Jenis": jenis,
            "Jumlah (Rp)": jumlah,
            "Catatan": catatan
        }
        st.session_state.data_tabungan = pd.concat([st.session_state.data_tabungan, pd.DataFrame([new_data])], ignore_index=True)
        st.sidebar.success("Data berhasil disimpan!")

# Ringkasan Saldo (Dashboard)
st.subheader("📊 Ringkasan Keuangan")

df = st.session_state.data_tabungan
if not df.empty:
    masuk = df[df["Jenis"] == "Tabungan Masuk"]["Jumlah (Rp)"].sum()
    keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah (Rp)"].sum()
    total_saldo = masuk - keluar

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Tabungan", f"Rp {masuk:,.0f}")
    col2.metric("Total Keluar", f"Rp {keluar:,.0f}")
    col3.metric("Saldo Bersih", f"Rp {total_saldo:,.0f}")

    # Tabel Riwayat Transaksi
    st.subheader("📜 Riwayat Transaksi")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data transaksi. Silakan input melalui menu di sebelah kiri (atau sidebar di HP).")
