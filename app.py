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

# Menentukan nama kolom kota & tahun secara terdeteksi otomatis
col_tahun_candidates = [c for c in df.columns if 'tahun' in c.lower()]
col_kota_candidates = [c for c in df.columns if 'kota' in c.lower() or 'kabupaten' in c.lower() or 'region' in c.lower()]

col_tahun = col_tahun_candidates[0] if col_tahun_candidates else df.columns[1]
col_kota = col_kota_candidates[0] if col_kota_candidates else df.columns[0]

# 3. SIDEBAR (PANEL FILTER & MENU)
st.sidebar.markdown("## 🔎 Filter Data")

# Filter Kota (Multiselect di bagian atas sidebar)
daftar_kota = sorted(df[col_kota].dropna().unique().tolist())
default_kota = ["Kota Banda Aceh", "Kota Sabang", "Kota Langsa", "Kota Lhokseumawe", "Kota Subulussalam"]
default_selected = [k for k in default_kota if k in daftar_kota]
if not default_selected:
    default_selected = daftar_kota[:5]

kota_terpilih = st.sidebar.multiselect(
    "Pilih Kota",
    options=daftar_kota,
    default=default_selected
)

# Filter Rentang Tahun (Slider)
min_thn = int(df[col_tahun].min()) if col_tahun in df.columns else 2014
max_thn = int(df[col_tahun].max()) if col_tahun in df.columns else 2024

rentang_tahun = st.sidebar.slider(
    "Rentang Tahun",
    min_value=min_thn,
    max_value=max_thn,
    value=(min_thn, max_thn)
)

st.sidebar.markdown("---")

# Menu Navigasi di Sidebar (Radio Button)
st.sidebar.markdown("## 📊 Dashboard Fiskal")
menu = st.sidebar.radio(
    "Pilih Menu",
    [
        "Beranda",
        "Data Fiskal",
        "Analisis Tren",
        "Perbandingan Kota",
        "Regresi OLS",
        "Tentang Dashboard"
    ]
)

# Filtering Dataframe
df_filtered = df[
    (df[col_tahun] >= rentang_tahun[0]) & 
    (df[col_tahun] <= rentang_tahun[1]) & 
    (df[col_kota].isin(kota_terpilih))
]

# 4. KONTEN UTAMA
st.title("💖 Dashboard Data Fiskal Kota Milik Zahra")
st.markdown("Visualisasi data penerimaan fiskal, belanja pemerintah, dan indikator sosial ekonomi berdasarkan kota dan tahun.")

st.markdown("---")

# Ringkasan Metrics
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

with col_m1:
    st.metric(label="Jumlah Observasi", value=f"{len(df_filtered):,}")

with col_m2:
    st.metric(label="Jumlah Kota", value=f"{df_filtered[col_kota].nunique()}")

with col_m3:
    st.metric(label="Jumlah Tahun", value=f"{df_filtered[col_tahun].nunique()}")

with col_m4:
    st.metric(label="Jumlah Variabel", value=f"{len(df_filtered.columns)}")

st.markdown("---")

# Tampilan berdasarkan Menu yang Dipilih / Tab Navigation
if menu == "Beranda" or menu == "Data Fiskal":
    tab_data, tab_tren, tab_stat, tab_kor = st.tabs([
        "📋 Data", 
        "📈 Tren", 
        "📊 Statistik", 
        "🔗 Korelasi"
    ])

    with tab_data:
        st.subheader("Tabel Dataset")
        st.dataframe(df_filtered, use_container_width=True)

    with tab_tren:
        st.subheader("Grafik Tren Variabel")
        numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
        if col_tahun in numeric_cols:
            numeric_cols.remove(col_tahun)
        
        var_pilihan = st.selectbox("Pilih Variabel Tren", numeric_cols)
        if not df_filtered.empty:
            df_trend = df_filtered.groupby(col_tahun)[var_pilihan].mean().reset_index()
            st.line_chart(df_trend.set_index(col_tahun))

    with tab_stat:
        st.subheader("Statistik Deskriptif")
        st.write(df_filtered.describe())

    with tab_kor:
        st.subheader("Matriks Korelasi")
        num_df = df_filtered.select_dtypes(include=[np.number])
        st.dataframe(num_df.corr(), use_container_width=True)

elif menu == "Analisis Tren":
    st.subheader("📈 Analisis Tren Waktu ke Waktu")
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    if col_tahun in numeric_cols:
        numeric_cols.remove(col_tahun)
    var_pilihan = st.selectbox("Pilih Variabel", numeric_cols)
    if not df_filtered.empty:
        df_trend = df_filtered.groupby(col_tahun)[var_pilihan].mean().reset_index()
        st.line_chart(df_trend.set_index(col_tahun))

elif menu == "Perbandingan Kota":
    st.subheader("📊 Perbandingan Variabel Antar Kota")
    numeric_cols = df_filtered.select_dtypes(include=[np.number]).columns.tolist()
    if col_tahun in numeric_cols:
        numeric_cols.remove(col_tahun)
    var_bar = st.selectbox("Pilih Variabel", numeric_cols)
    if not df_filtered.empty:
        df_bar = df_filtered.groupby(col_kota)[var_bar].mean().reset_index()
        st.bar_chart(df_bar.set_index(col_kota))

elif menu == "Regresi OLS":
    st.subheader("🔬 Analisis Regresi OLS")
    st.write("Ringkasan statistik data untuk pemodelan regresi:")
    st.write(df_filtered.describe())

elif menu == "Tentang Dashboard":
    st.subheader("ℹ️ Tentang Dashboard")
    st.write("Dashboard ini dibuat oleh **Zahra** untuk menyajikan data fiskal dan makroekonomi 97 Kota di Indonesia.")
