import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import plotly.express as px
import plotly.graph_objects as go

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

    .block-container { position: relative; z-index: 1; }

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

    .modern-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        border: 1px solid rgba(240, 228, 225, 0.8);
        margin-bottom: 20px;
    }

    .bank-card {
        background: linear-gradient(135deg, #ffffff 0%, #fdfbf7 100%);
        border: 2px dashed #d4a39f;
        padding: 18px;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    }

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

    <div class="floating-hearts">
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
        <div class="heart"></div><div class="heart"></div><div class="heart"></div>
    </div>
""", unsafe_allow_html=True)

# 🔗 LINK WEB APP GOOGLE SCRIPT KAMU
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxbpS8vKgt3cOXfu8pLfP_HWUcRXYejebTRVtVmDsmUb6Q4zwX7a_5HmEo7L1ci5n-o/exec"

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

if not df.empty and "Jumlah" in df.columns:
    df["Jumlah"] = pd.to_numeric(df["Jumlah"], errors="coerce").fillna(0)
    masuk = df[df["Jenis"] == "Tabungan Masuk"]["Jumlah"].sum()
    keluar = df[df["Jenis"] == "Pengeluaran"]["Jumlah"].sum()
    total_saldo = masuk - keluar
else:
    masuk = 0
    keluar = 0
    total_saldo = 0

TARGET_NIKAH = 50000000 
progress = min(total_saldo / TARGET_NIKAH, 1.0) if TARGET_NIKAH > 0 else 0

# Banner Utama
st.markdown("""
    <div class="banner-card">
        <div style="font-size: 2.5rem; margin-bottom: 5px;">💍👩‍❤️‍👨👰‍♀️</div>
        <div class="banner-title">Nikah Sama Sayang Fira & Syaiful</div>
        <p style="color: #fefefe; font-size: 0.95rem; margin: 0; font-weight: 500;">Menuju lembaran baru yang sakinah, mawaddah, warahmah ✨</p>
    </div>
""", unsafe_allow_html=True)

# Card Rekening Bank
st.markdown("""
    <div class="bank-card">
        <p style="color: #8c6d6b; margin: 0 0 5px 0; font-size: 0.85rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">💳 Rekening Tujuan Nabung</p>
        <h3 style="color: #5e4644; margin: 0; font-weight: 800;">🏦 Mandiri : <code>1430036629572</code></h3>
        <p style="color: #666; margin: 5px 0 0 0; font-size: 0.95rem; font-weight: 500;">a.n. <b>Magfiroh Izzani Aulia Putri</b></p>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Dashboard Kombinasi & Analisis", "📜 Riwayat Transaksi"])

with tab1:
    st.markdown("""
        <div class="modern-card" style="text-align: center;">
            <span class="badge-on-track">ON TRACK ✨</span>
            <p style="color: #8c6d6b; margin-bottom: 5px; font-size: 0.9rem; font-weight: 600;">Total Tabungan Terkumpul</p>
            <h1 style="color: #5e4644; font-weight: 800; margin-top: 0;">Rp {:,.0f}</h1>
            <p style="color: #a3918f; font-size: 0.85rem;">dari target Rp {:,.0f}</p>
        </div>
    """.format(total_saldo, TARGET_NIKAH), unsafe_allow_html=True)

    st.progress(progress)
    st.caption(f"Pencapaian: **{progress * 100:.1f}%** dari total target impian.")
    
    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("💖 Tabungan Masuk", f"Rp {masuk:,.0f}")
    with col_b:
        st.metric("🛍️ Total Keluar", f"Rp {keluar:,.0f}")

with tab2:
    st.markdown("<h3 style='color: #8c6d6b;'>📈 Dashboard Kombinasi Keuangan (Pemasukan vs Pengeluaran)</h3>", unsafe_allow_html=True)
    
    if not df.empty:
        # Menyiapkan data gabungan untuk Plotly
        # Ringkasan Pemasukan per Orang/Sumber
        df_masuk = df[df["Jenis"] == "Tabungan Masuk"]
        df_keluar = df[df["Jenis"] == "Pengeluaran"]
        
        sum_masuk = df_masuk.groupby("Nama")["Jumlah"].sum().reset_index()
        sum_masuk["Kategori"] = sum_masuk["Nama"]
        sum_masuk["Tipe"] = "Tabungan Masuk"
        
        sum_keluar = df_keluar.groupby("Catatan")["Jumlah"].sum().reset_index()
        sum_keluar.rename(columns={"Catatan": "Kategori"}, inplace=True)
        sum_keluar["Tipe"] = "Pengeluaran"
        
        df_combined = pd.concat([sum_masuk, sum_keluar], ignore_index=True)
        
        if not df_combined.empty:
            # Membuat Grafik Kombinasi Interaktif dengan Plotly (Bar Chart + Line Chart)
            fig = px.bar(
                df_combined, 
                x="Kategori", 
                y="Jumlah", 
                color="Tipe", 
                barmode="group",
                color_discrete_map={"Tabungan Masuk": "#d4a39f", "Pengeluaran": "#bc8a86"},
                text_auto=',.0f'
            )
            
            # Tambahan garis tren (Line Chart) di atas bar chart agar mirip contoh referensi
            fig.add_trace(
                go.Scatter(
                    x=df_combined["Kategori"],
                    y=df_combined["Jumlah"],
                    mode="lines+markers",
                    name="Tren Nominal",
                    line=dict(color="#5e4644", width=3)
                )
            )
            
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Inter", color="#5e4644"),
                margin=dict(t=20, b=20, l=20, r=20),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("<hr style='border:0; height:1px; background:#f0e4e1; margin: 20px 0;'>", unsafe_allow_html=True)
        
        # Tabel Ringkasan Rinci dengan Persentase Desimal ala Dashboard Eksekutif
        col_tabel1, col_tabel2 = st.columns(2)
        
        with col_tabel1:
            st.markdown("#### 💖 Detail Pemasukan")
            if not df_masuk.empty:
                p_group = df_masuk.groupby("Nama")["Jumlah"].sum()
                tot_m = p_group.sum()
                for k, v in p_group.items():
                    pct = (v / tot_m * 100) if tot_m > 0 else 0
                    st.markdown(f"- **{k}**: Rp {v:,.0f} *({pct:.2f}%)*")
            else:
                st.info("Belum ada data pemasukan.")
                
        with col_tabel2:
            st.markdown("#### 🛍️ Detail Pengeluaran")
            if not df_keluar.empty:
                k_group = df_keluar.groupby("Catatan")["Jumlah"].sum()
                tot_k = k_group.sum()
                for k, v in k_group.items():
                    pct = (v / tot_k * 100) if tot_k > 0 else 0
                    cat_name = k if k else "Lain-lain"
                    st.markdown(f"- **{cat_name}**: Rp {v:,.0f} *({pct:.2f}%)*")
            else:
                st.info("Belum ada data pengeluaran.")
                
    else:
        st.info("Belum ada data transaksi untuk dianalisis.")

with tab3:
    st.markdown("<h3 style='color: #8c6d6b;'>📜 Riwayat Transaksi Lengkap</h3>", unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data transaksi yang tercatat.")

# Sidebar untuk Input Data
st.sidebar.markdown("<h2 style='color: #8c6d6b;'>✨ Tambah Catatan</h2>", unsafe_allow_html=True)
with st.sidebar.form("form_tabungan", clear_on_submit=True):
    tanggal = st.date_input("Tanggal", datetime.today())
    nama = st.selectbox("Penyetor / Pengambil", ["Syaiful", "Fira"])
    jenis = st.selectbox("Jenis Transaksi", ["Tabungan Masuk", "Pengeluaran"])
    jumlah = st.number_input("Nominal (Rp)", min_value=0, step=50000)
    catatan = st.text_input("Catatan (contoh: Gaji Syaiful / Beli Undangan)", placeholder="cth: Gaji Bulanan / Beli Cincin")
    
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
