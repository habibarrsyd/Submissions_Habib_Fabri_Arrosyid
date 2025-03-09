import streamlit as st
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset (sesuaikan lokasi dataset jika perlu)
df_hour = pd.read_csv("data/hour.csv")  
df_day = pd.read_csv("data/day.csv")

# Mapping musim dan kondisi cuaca
season_mapping = {1: "Semi", 2: "Panas", 3: "Gugur", 4: "Dingin"}
weather_mapping = {1: "Cerah", 2: "Kabut Berawan", 3: "Hujan Ringan"}

# Menyiapkan dataset untuk analisis
df_season = df_day[['cnt', 'season', 'weathersit']]
df_season["season"] = df_season["season"].map(season_mapping)
df_season["weathersit"] = df_season["weathersit"].map(weather_mapping)

# Data agregasi berdasarkan musim dan cuaca
agg_data = df_season.groupby(["season", "weathersit"])["cnt"].mean().reset_index()

# Streamlit UI
st.title('Analisis Data - Bike Sharing Dataset')

# Sidebar
with st.sidebar:
    st.header("Tentang Dataset")
    st.write("Dataset ini berisi informasi penyewaan sepeda berdasarkan waktu, cuaca, dan hari kerja/akhir pekan.")
    st.write("- **hour.csv**: Data penyewaan sepeda per jam.")
    st.write("- **day.csv**: Data penyewaan sepeda per hari.")
    
    # Select tab
    selected_tab = st.selectbox("Pilih Analisis:", ["Question 1", "Question 2", "Question 3"])

# Menyiapkan data untuk jam sibuk
hourly_workingday = df_hour[df_hour["workingday"] == 1].groupby("hr")["cnt"].mean()
hourly_weekend = df_hour[df_hour["workingday"] == 0].groupby("hr")["cnt"].mean()

# Question 1: Pola penggunaan berdasarkan jam sibuk
if selected_tab == "Question 1":
    st.header("Apakah ada pola penggunaan yang menunjukkan jam-jam sibuk dan sepi?")
    
    # Slider untuk memilih rentang jam
    time_range = st.slider("Pilih rentang waktu (jam)", 0, 23, (0, 23))
    
    filtered_workingday = hourly_workingday[time_range[0]:time_range[1]+1]
    filtered_weekend = hourly_weekend[time_range[0]:time_range[1]+1]
    
    with st.container():
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(filtered_workingday.index, filtered_workingday.values, marker="o", linestyle="-", color="blue", label="Hari Kerja")
        ax.plot(filtered_weekend.index, filtered_weekend.values, marker="o", linestyle="-", color="red", label="Akhir Pekan")
        
        ax.set_xticks(range(time_range[0], time_range[1]+1))
        ax.set_xlabel("Jam")
        ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda")
        ax.set_title("Perbandingan Pola Penyewaan Sepeda: Hari Kerja vs. Akhir Pekan")
        ax.legend()
        ax.grid()
        
        st.pyplot(fig)
    with st.expander("See explanation"):
        st.write(
            """
            Insight Keseluruhan Dari grafik, terlihat pola penggunaan sepeda yang berbeda antara hari kerja (garis biru) dan akhir pekan (garis merah):

1. Jam Sibuk (Peak Hours)
Hari kerja:
- Pagi (07:00 - 09:00) → Lonjakan besar, mencapai puncak sekitar pukul 08:00. Ini menunjukkan bahwa banyak pengguna menggunakan sepeda untuk perjalanan ke tempat kerja atau sekolah.
- Sore (17:00 - 19:00) → Puncak lain terjadi sekitar 18:00, yang mencerminkan perjalanan pulang dari kantor/sekolah.
Akhir pekan:
- Siang hingga sore (10:00 - 17:00) → Aktivitas penyewaan meningkat secara bertahap dan tetap tinggi hingga sore hari. Tidak ada lonjakan tajam seperti di hari kerja, tetapi penggunaannya lebih stabil.
2. Jam Sepi (Off-Peak Hours)
- Dini hari hingga pagi (00:00 - 05:00) → Penggunaan sangat rendah di kedua kategori, karena jam ini biasanya bukan waktu perjalanan utama.
- Hari kerja antara jam 09:00 - 16:00 → Penyewaan cenderung lebih rendah dibandingkan jam sibuk pagi dan sore, menunjukkan bahwa sebagian besar pengguna sudah berada di tempat kerja atau sekolah.

Indikasi : 

Hari kerja menunjukkan pola yang khas untuk komuter, dengan dua lonjakan tajam di pagi dan sore hari.
Akhir pekan memiliki pola penggunaan yang lebih merata sepanjang siang dan sore, menunjukkan penggunaan untuk rekreasi atau perjalanan santai.
Jam-jam sepi terjadi di dini hari dan pagi buta (00:00 - 05:00), serta di antara jam sibuk pada hari kerja."""
        )

# Question 2: Pola penyewaan berdasarkan cuaca dan musim
elif selected_tab == "Question 2":
    st.header("Apakah ada pola penyewaan berdasarkan kondisi cuaca dan musim?")
    
    selected_season = st.selectbox("Pilih Musim:", list(season_mapping.values()))
    
    filtered_agg = agg_data[agg_data["season"] == selected_season]
    
    with st.container():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=filtered_agg, x="season", y="cnt", hue="weathersit", 
                    palette=["lightgreen", "gold", "red"], edgecolor="black", ax=ax)
        ax.set_title("Rata-rata Penyewaan Sepeda Berdasarkan Musim dan Kondisi Cuaca")
        ax.set_xlabel("Musim")
        ax.set_ylabel("Rata-rata Jumlah Penyewaan")
        st.pyplot(fig)
    with st.expander("Lihat Penjelasan"):
        st.write("""
                 Insight keseluruhan yang didapatkan : 

        **1. Cuaca Cerah Mendorong Penyewaan Tertinggi**  
        Jumlah penyewaan sepeda selalu tertinggi dalam kondisi cerah, terlepas dari musim. 
        Ini menunjukkan bahwa pengguna lebih cenderung menggunakan sepeda sebagai moda transportasi atau rekreasi saat cuaca mendukung.

        **2. Musim Panas dan Gugur Adalah Puncak Penyewaan**  
        Penyewaan sepeda mencapai puncaknya pada musim panas dan gugur, terutama saat cuaca cerah. 
        Hal ini bisa disebabkan oleh liburan musim panas, cuaca yang lebih nyaman, dan kemungkinan lebih banyak orang yang beraktivitas di luar ruangan.

        **3. Musim Dingin Memiliki Penyewaan yang Relatif Tinggi**  
        Meskipun cuaca dingin biasanya mengurangi aktivitas luar ruangan, penyewaan sepeda tetap cukup tinggi, terutama dalam kondisi cerah dan kabut berawan. 
        Ini bisa menunjukkan bahwa pengguna di musim dingin lebih didominasi oleh komuter (pengguna harian) daripada pengguna rekreasi.
        
        **4. Hujan Ringan Menyebabkan Penurunan Signifikan**

        Saat hujan ringan, jumlah penyewaan turun drastis di semua musim, tetapi penurunannya tidak terlalu tajam di musim gugur dibandingkan musim lainnya.
        Ini bisa mengindikasikan bahwa di musim gugur, pengguna mungkin lebih siap menghadapi hujan ringan, atau ada faktor lain seperti frekuensi hujan yang lebih tinggi di musim lain yang menyebabkan dampak lebih besar.

        **5. Perbedaan Tajam antara Musim Semi dan Panas** 

        Terdapat perbedaan besar dalam jumlah penyewaan antara musim semi dan musim panas, terutama dalam kondisi cerah dan kabut berawan.
        Hal ini bisa menunjukkan bahwa cuaca yang lebih hangat mendorong lebih banyak orang untuk menggunakan sepeda dibandingkan saat suhu masih relatif dingin di musim semi.
                 """)

# Question 3: Perbandingan pengguna kasual dan terdaftar
elif selected_tab == "Question 3":
    st.header("Bagaimana pola penggunaan sepeda antara pengguna kasual dan terdaftar?")
    
    agg_data = df_day.groupby(['workingday'])[['casual', 'registered']].sum().reset_index()
    agg_data['workingday'] = agg_data['workingday'].map({0: 'Akhir Pekan', 1: 'Hari Kerja'})
    
    # Opsi pilihan pengguna
    user_type = st.radio("Pilih Tipe Pengguna:", ("Kedua-duanya", "Casual", "Registered"))
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    if user_type == "Casual":
        ax.bar(agg_data["workingday"], agg_data["casual"], color='skyblue', label="Casual Users")
    elif user_type == "Registered":
        ax.bar(agg_data["workingday"], agg_data["registered"], color='orange', label="Registered Users")
    else:
        ax.bar(agg_data["workingday"], agg_data["casual"], color='skyblue', label="Casual Users")
        ax.bar(agg_data["workingday"], agg_data["registered"], color='orange', bottom=agg_data["casual"], label="Registered Users")
    
    ax.set_xlabel("Tipe Hari")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Perbandingan Pengguna Kasual dan Terdaftar")
    ax.legend()
    st.pyplot(fig)

    # Slider untuk memilih rentang bulan
    month_range = st.slider("Pilih Rentang Bulan", 1, 12, (1, 12))
    
    df_filtered = df_day[(df_day["mnth"] >= month_range[0]) & (df_day["mnth"] <= month_range[1])]
    
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df_filtered, x="mnth", y="casual", label="Casual Users", marker="o", color='blue', ax=ax)
    sns.lineplot(data=df_filtered, x="mnth", y="registered", label="Registered Users", marker="o", color='orange', ax=ax)
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Tren Penyewaan Pengguna Kasual vs Terdaftar per Bulan")
    ax.legend()
    st.pyplot(fig)
    with st.expander("See explanation"):
        st.write("""
                 Insight keseluruhan yang didapatkan :
        Dari kedua grafik di atas, kita bisa melihat pola penggunaan sepeda antara pengguna kasual dan pengguna terdaftar:

1. Perbandingan Pengguna Kasual vs Terdaftar pada Hari Kerja vs Akhir Pekan (Grafik 1)
- Pada hari kerja, mayoritas penyewaan sepeda dilakukan oleh pengguna terdaftar, sementara pengguna kasual hanya menyumbang bagian kecil.
- Pada akhir pekan, proporsi pengguna kasual meningkat secara signifikan, meskipun pengguna terdaftar masih mendominasi.

Insight:

- Pengguna terdaftar cenderung menggunakan sepeda untuk keperluan rutin, seperti komuter harian.
- Pengguna kasual lebih banyak menggunakan sepeda pada akhir pekan, kemungkinan untuk rekreasi atau aktivitas santai.

2. Tren Penyewaan Pengguna Kasual vs Terdaftar per Bulan (Grafik 2)
- Tren penyewaan pengguna terdaftar menunjukkan pola yang lebih tinggi dan stabil sepanjang tahun, dengan puncak pada bulan pertengahan tahun (Mei - Agustus).
- Pengguna kasual juga mengalami peningkatan di pertengahan tahun, meskipun jumlahnya jauh lebih kecil dibanding pengguna terdaftar.

Insight:

- Puncak peminjaman terjadi pada musim panas (pertengahan tahun), menunjukkan bahwa kondisi cuaca dan liburan mungkin berpengaruh.
- Pengguna kasual mengalami peningkatan yang lebih tajam dibandingkan pengguna terdaftar pada bulan-bulan tertentu, mengindikasikan bahwa kasual lebih terpengaruh oleh faktor musiman.
- Pengguna terdaftar tetap aktif sepanjang tahun, menunjukkan kebiasaan penggunaan reguler.

Kesimpulan :
- Pengguna kasual lebih cenderung menyewa sepeda pada akhir pekan dan bulan-bulan hangat, kemungkinan besar untuk keperluan rekreasi.
- Pengguna terdaftar lebih konsisten dalam penyewaan sepanjang tahun dan lebih aktif di hari kerja, menunjukkan bahwa mereka menggunakan sepeda sebagai bagian dari rutinitas harian, seperti transportasi ke kantor atau sekolah.
- Faktor musim, cuaca, dan hari dalam seminggu memiliki pengaruh signifikan terhadap pola penggunaan sepeda, terutama untuk pengguna kasual.""")

