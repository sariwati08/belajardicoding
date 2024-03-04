import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='whitegrid')

#Membuat helper function
def create_daily_used_df(df):
    daily_used_df = all_df.resample(rule='M', on='dteday').agg({
        "cnt": "sum"
    })
    daily_used_df.index = daily_used_df.index.strftime('%Y-%m')
    daily_used_df = daily_used_df.reset_index()

    daily_used_df.rename(columns={
        "cnt": "jumlah_pengguna"
    }, inplace=True)
    return daily_used_df

def create_windspeed_used_df(df):
    windspeed_used_df = all_df.groupby('windspeed').agg({
        "cnt": "sum"
    })
    windspeed_used_df=windspeed_used_df.reset_index()
    return windspeed_used_df

#Load berkas all_data.csv sebagai sebuah DataFrame
all_df = pd.read_csv("all_data.csv")

#Ubah type data pada dteday dari objek menjadi datetime
all_df['dteday'] = pd.to_datetime(all_df['dteday'])

#Membuat Komponen Filter
min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

#Data yang telah difilter selanjutnya akan disimpan dalam main_df.
main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date))]

#Membuat Visualisasi data
daily_used_df = create_daily_used_df(main_df)
windspeed_used_df = create_windspeed_used_df(main_df)

#Membuat header
st.header('Dicoding Bike-Sharing :sparkles:')

#Membuat subheader(1)
st.subheader('Performa Dicoding Bike-Sharing 2011-2012')
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_used_df["dteday"],
    daily_used_df["jumlah_pengguna"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15, rotation = 45)
 
st.pyplot(fig)


#Membuat subheader(2)
st.subheader('Penggunaan Sepeda Berdasarkan Musim (Pie Chart dan Bar)')

col1, col2 = st.columns(2)
 
season_used_df = all_df.groupby('season').agg({
    "cnt": "sum"
})
season_used_df=season_used_df.reset_index()

with col1:
    fig, ax = plt.subplots(figsize=(10, 10))
    plt.bar(x='season', height='cnt', data= season_used_df,color='skyblue')
    plt.xlabel('Musim')
    plt.ylabel('Jumlah Sepeda Disewa')
    plt.xticks(ticks=season_used_df['season'], labels=['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin'], fontsize =20)
    st.pyplot(fig)
with col2:
    fig, ax = plt.subplots(figsize=(15, 15))
    Nama = ('Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Dingin')
    plt.pie(x='cnt', data=season_used_df, labels= Nama, autopct='%1.1f%%')
    plt.axis('equal')
    st.pyplot(fig)

#Membuat subheader(3)
st.subheader('Korelasi antara Kecepatan Angin dan Jumlah Sewa Sepeda')
fig, ax = plt.subplots(figsize=(20, 10))
sns.regplot(x='windspeed', y='cnt', data=windspeed_used_df, color='skyblue', ax =ax)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)