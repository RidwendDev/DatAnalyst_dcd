import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
sns.set(style='dark')

# Menampilkan judul pada dashboard
st.markdown("<h1 style='text-align: center;'>Air Quality in China: How Bad Is It?</h1>", unsafe_allow_html=True)



combined_df = pd.read_csv(r'comb_data.csv')
print(combined_df.info())

# Menghitung statistik ringkasan
mean_pm25 = combined_df['PM2.5'].mean()
median_pm25 = combined_df['PM2.5'].median()
max_pm25 = combined_df['PM2.5'].max()
min_pm25 = combined_df['PM2.5'].min()

# Menampilkan statistik ringkasan dengan format yang lebih baik
st.markdown('## Statistik Ringkasan 📊')
st.info(f"Rata-rata PM2.5: **{round(mean_pm25, 2)}**")
st.warning(f"Median PM2.5: **{median_pm25}**")
st.error(f"Maksimum PM2.5: **{max_pm25}**")
st.success(f"Minimum PM2.5: **{min_pm25}**")

st.write(' ')
st.write(' ')
st.markdown('### CO vs PM2.5 💨 ')
def create_reg_plot(data, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    sns.regplot(x=combined_df['PM2.5'], y=combined_df['CO'])
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    # Menyembunyikan peringatan PyplotGlobalUseWarning
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Menampilkan plot di Streamlit
    st.pyplot()

create_reg_plot(combined_df,'Partikel PM2.5 (PM2.5)','Karbon Monoksida (CO)','Hubungan Antara Partikel PM2.5 dan Karbon Monoksida')

st.write(' ')
st.write(' ')
st.write('Dari sini kita dapat melihat bahwasanya Polutan Karbon Monoksida berkorelasi cukup tinggi dengan Partikel PM2.5, jadi kita akan fokuskan lebih ke tren waktu tingkat CO di setiap kota seperti dibawah ini.')

st.markdown('## Filter Tren Waktu Tingkat CO di Tiap Kota 🌁 ')
# Filter berdasarkan Kota
selected_city = st.selectbox('Pilih Kota', combined_df['station'].unique())

# Filter berdasarkan Tingkat CO
co_min = st.slider('Tingkat CO Minimum', min_value=100.0, max_value=10000.0, step=0.1)
co_max = st.slider('Tingkat CO Maximum', min_value=100.0, max_value=10000.0, step=0.1, value=100.0)

# Terapkan filter
filtered_data = combined_df[(combined_df['station'] == selected_city) & (combined_df['CO'] >= co_min) & (combined_df['CO'] <= co_max)]

# Tampilkan data terfilter
st.dataframe(filtered_data)

# Tampilkan plot terfilter
fig, ax = plt.subplots()
sns.lineplot(data=filtered_data, x='hour', y='CO', ax=ax)
ax.set_xlabel('Jam')
ax.set_ylabel('Tingkat CO')
ax.set_title(f'Tren Waktu Tingkat CO di Kota {selected_city}')
plt.xticks(rotation=45)
st.pyplot(fig)


st.markdown('## Top yang (tidak) Top 🔝 ')
# Fungsi untuk membuat bar plot
def create_bar_plot(data, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    sns.barplot(x=data.index, y=data.values)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xticks(rotation=45)
    plt.title(title)

    # Menyembunyikan peringatan PyplotGlobalUseWarning
    st.set_option('deprecation.showPyplotGlobalUse', False)

    # Menampilkan plot di Streamlit
    st.pyplot()

# Menghitung rata-rata tingkat partikel PM2.5 per kota
average_pm25 = combined_df.groupby('station')['PM2.5'].mean().sort_values(ascending=False)

# Mengambil 10 kota dengan tingkat polusi tertinggi
top_cities = average_pm25.head(10)

# Memanggil fungsi untuk membuat bar plot
create_bar_plot(top_cities, 'Kota', 'Rata-rata PM2.5', 'Top 10 Kota dengan Tingkat Polusi Tertinggi')



teks_bar1 = st.write('''Ini adalah bar plot untuk kota dengan tingkat polusi tertinggi. Kita dapat melihat bahwa
                untuk kota dengan tingkat PM2.5 tertinggi dipegang oleh Dongsi diikuti oleh Wanshouxigong
                dan kota dengan tingkat polusi terendah adalah Changping. Adapun faktor yang umumnya menyebabkan
                polusi tinggi adalah aktivitas industri, lalu lintas kendaraan dan yang tak kalah penting
                adalah kebijakan dan pemantauan lingkungan dari pemerintah''')

# Menampilkan teks di Streamlit
st.text(teks_bar1)


# Fungsi untuk membuat line plot
def create_line_plot(data, x_label, y_label, title):
    for column in data.columns:
        sns.lineplot(x=data.index, y=data[column], label=column)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.legend()

    # Menampilkan plot di Streamlit
    st.pyplot()


st.markdown('#### 🕙 Tren Waktu vs Tingkat Partikel PM2.5 untuk Semua Kota 🕝')
# Menggunakan st.beta_columns() untuk membagi layar menjadi dua kolom
left_column, right_column = st.columns(2)

# Melakukan pivot tabel untuk mengubah kolom 'station' menjadi kolom-kolom yang mewakili setiap kota
pivot_df_month_station = combined_df.pivot_table(index='month', columns='station', values='PM2.5')

# Melakukan pivot tabel untuk mengubah kolom 'station' menjadi kolom-kolom yang mewakili setiap kota
pivot_df_hour_station = combined_df.pivot_table(index='hour', columns='station', values='PM2.5')

# Menampilkan line plot bulanan di samping kiri
with left_column:
    fig, ax = plt.subplots(figsize=(10, 6))
    create_line_plot(pivot_df_month_station, 'Bulan', 'Tingkat Rata-rata PM2.5', 'Tren Waktu (Bulan) Tingkat Partikel PM2.5 untuk Semua Kota')

# Menampilkan line plot per jam di samping kanan
with right_column:
    fig, ax = plt.subplots(figsize=(10, 6))
    create_line_plot(pivot_df_hour_station, 'Jam', 'Tingkat Rata-rata PM2.5', 'Tren Waktu (Jam) Tingkat Partikel PM2.5 untuk Semua Kota')


st.write("Disini kita dapat melihat pattern dimana sebagian besar kota mengalami peningkatan di bulan ketiga (Maret) dan berikutnya naik turun, tetapi di akhir tahun angka PM2.5 terus meningkat puncaknya di bulan terakhir (Desember). Adapun faktor yang menyebabkan antara lain:")
st.write("- Perubahan cuaca dan musim dapat mempengaruhi pergerakan dan dispersi partikel polutan di udara. Pada musim dingin, polutan seperti PM2.5 dapat terjebak di permukaan tanah karena kondisi inversi termal atau pola pergerakan udara yang lebih terbatas, sehingga menyebabkan peningkatan konsentrasi polutan.")
st.write("- Peningkatan aktivitas pemanasan dan pembakaran bahan bakar di musim dingin, terutama pada area dengan cuaca dingin, dapat meningkatkan emisi polutan seperti PM2.5. Penggunaan alat pemanas, seperti tungku kayu atau sistem pemanas ruangan, dapat berkontribusi terhadap peningkatan polusi udara.")

st.write(" ")
st.write(" ")

st.write("Disini kita dapat melihat pattern yang hampir sama dimana ada jam-jam yang cenderung terjadi peningkatan PM2.5, Mungkin sebagian besar orang akan berpikir di pagi hari terjadi kenaikan besar-besaran tetapi hal itu tidak terjadi(Based in data) malah di malam hari sampai dini hari tepatnya jam 21.00 keatas angka PM2.5 terus meningkat. Adapun faktor yang menyebabkan antara lain:")
st.write("- Faktor cuaca seperti inversi termal atau kondisi atmosfer yang stabil pada malam hari dapat menyebabkan penumpukan polutan di permukaan dan meningkatkan konsentrasi polusi PM2.5. Jika kondisi cuaca menghambat dispersi polutan, polusi dapat meningkat pada malam hari.")
st.write("- Pola penggunaan energi juga dapat berdampak pada polusi PM2.5. Pada malam hari, ketika kebutuhan penerangan dan pendinginan rumah meningkat, penggunaan listrik dan sistem pendingin dapat menyebabkan peningkatan emisi polutan, seperti partikel PM2.5.")
