import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title("🚀 Visualisasi Penjualan Listrik Berdasarkan Tahun")

# URL raw CSV file di GitHub
csv_url = "https://github.com/lintangbhskr/streamlit_bps/blob/main/data_pln_clean.csv"  # Ganti dengan URL raw GitHub Anda

# Fungsi untuk memuat data dari GitHub
@st.cache
def load_data():
    df = pd.read_csv(csv_url)
    return df

# Muat data
df = load_data()

# Cek data berhasil dimuat
st.success("✅ Data berhasil dimuat dari GitHub!")

# Tampilkan kolom yang ada dalam dataset
st.write("Kolom dalam dataset:", df.columns)

# Pastikan kolom yang diperlukan ada
if all(col in df.columns for col in ['Produksi_kWh', 'Terjual_kWh', 'Efficiency_', 'Kesusutan_kWh', 'Persentase_', 'Pelanggan', 'Tahun']):
    
    # 1. Pilihan SelectBox untuk memilih Tahun
    years = df["Tahun"].unique()  # Ambil nilai unik dari kolom 'Tahun'
    selected_year = st.selectbox("Pilih Tahun untuk Analisis", years)

    # Filter data berdasarkan tahun yang dipilih
    df_filtered = df[df["Tahun"] == selected_year]

    # Tampilkan data yang dipilih
    st.write(f"Data untuk Tahun {selected_year}:")
    st.dataframe(df_filtered)

    # 2. Tren Produksi dan Listrik Terjual
    st.subheader("📈 Tren Produksi dan Listrik Terjual")
    if "YearMonth" not in df_filtered.columns:
        df_filtered['YearMonth'] = pd.to_datetime(df_filtered['Tahun'].astype(str) + df_filtered['Bulan'].astype(str), format='%Y%m')
    
    fig_prod_sales = px.line(df_filtered, x='YearMonth', y=['Produksi_kWh', 'Terjual_kWh'], title="Tren Produksi dan Listrik Terjual")
    st.plotly_chart(fig_prod_sales)
    st.divider()

    # 3. Tren Efisiensi Sistem
    st.subheader("📉 Tren Efisiensi Sistem")
    if "Efficiency_" in df_filtered.columns:
        fig_efficiency = px.line(df_filtered, x='YearMonth', y='Efficiency_', title="Tren Efisiensi Sistem Listrik")
        st.plotly_chart(fig_efficiency)
        st.divider()

    # 4. Analisis Susut Listrik
    st.subheader("📊 Analisis Susut Listrik")
    if "Kesusutan_kWh" in df_filtered.columns and "Persentase_" in df_filtered.columns:
        fig_loss = px.area(df_filtered, x='YearMonth', y=['Kesusutan_kWh', 'Persentase_'], 
                           title="Analisis Susut Listrik (kWh dan Persentase Susut)")
        st.plotly_chart(fig_loss)
        st.divider()

    # 5. Pertumbuhan Pelanggan vs Konsumsi Per Pelanggan
    st.subheader("📈 Pertumbuhan Pelanggan vs Konsumsi Per Pelanggan")
    if "Pelanggan" in df_filtered.columns and "Terjual_kWh" in df_filtered.columns:
        df_filtered['Konsumsi_per_Pelanggan'] = df_filtered['Terjual_kWh'] / df_filtered['Pelanggan']
        
        # Grafik konsumsi per pelanggan
        fig_growth_vs_consumption = px.bar(df_filtered, x="YearMonth", y="Konsumsi_per_Pelanggan", 
                                           title="Konsumsi Per Pelanggan (Terjual / Pelanggan)")
        st.plotly_chart(fig_growth_vs_consumption)
        st.divider()

        # Grafik pertumbuhan pelanggan
        fig_growth = px.line(df_filtered, x="YearMonth", y="Pelanggan", title="Pertumbuhan Jumlah Pelanggan")
        st.plotly_chart(fig_growth)
        st.divider()

else:
    st.error("Beberapa kolom yang dibutuhkan tidak ditemukan dalam dataset.")
