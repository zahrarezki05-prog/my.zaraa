import streamlit as st
import pandas as pd
import numpy as np

# 1. Konfigurasi Halaman (Harus di paling atas)
st.set_page_config(
    page_title="Dashboard Data Fiskal Kota Milik Zahra",
    page_icon="💖",
    layout="wide"
)

# 2. Fungsi Load Data dari GitHub Dosen
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Alam-A99/DATAAKSI/refs/heads/main/dataset_fiskal_97_hipoFull.csv"
    df = pd.read_csv(url)
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset: {e}")
    st.stop()

# 3. Judul dan Header Dashboard
st.title("📊 Dashboard Interaktif Data Fiskal & Makroekonomi 97 Kota")
st.markdown("Dibuat oleh **Zahra Rezki Dzakirah** | Visualisasi Data Fiskal Daerah")
st.markdown("---")

# 4. Sidebar untuk Filter
st.sidebar.header("🔍 Panel Filter Data")

# Cek kolom yang tersedia di dataset untuk filter
columns = df.columns.tolist()

# Contoh filter interaktif (menyesuaikan kolom kota/kabupaten dan tahun jika ada)
if 'nama_kota' in df.columns or 'Kota' in df.columns or 'kabupaten_kota' in df.columns:
    col_kota = [c for c in ['nama_kota', 'Kota', 'kabupaten_kota'] if c in df.columns][0]
    daftar_kota = sorted(df[col_kota].dropna().unique())
    selected_kota = st.sidebar.multiselect("Pilih Kota/Kabupaten:", daftar_kota, default=daftar_kota[:5])
    if selected_kota:
        df = df[df[col_kota].isin(selected_kota)]

# 5. Tampilan Utama (Multi-tab)
tab1, tab2, tab3 = st.tabs(["📈 Ringkasan & Statistik", "📋 Tabel Data Mentah", "📉 Grafik Analisis"])

with tab1:
    st.subheader("Ringkasan Statistik Dataset Fiskal")
    st.metric(label="Total Baris Data Ditampilkan", value=f"{df.shape[0]:,} baris")
    st.metric(label="Total Variabel/Kolom", value=f"{df.shape[1]} kolom")
    st.dataframe(df.describe(), use_container_width=True)

with tab2:
    st.subheader("Eksplorasi Data Mentah (Raw Data)")
    st.dataframe(df, use_container_width=True)

with tab3:
    st.subheader("Visualisasi Grafik Sederhana")
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) >= 2:
        x_axis = st.selectbox("Pilih Sumbu X:", numeric_cols, index=0)
        y_axis = st.selectbox("Pilih Sumbu Y:", numeric_cols, index=1)
        st.line_chart(df, x=x_axis, y=y_axis)
    else:
        st.info("Kolom numerik tidak cukup untuk membuat grafik.")

# Footer
st.markdown("---")
st.caption("© 2026 - Dashboard Fiskal Kota | Universitas Negeri Makassar")
