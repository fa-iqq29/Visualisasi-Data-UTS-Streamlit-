import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

# Load data dari file UTS yang kamu unggah
df = pd.read_excel('Southwind.xlsx', sheet_name='Orders')
# Cek isi data
st.title('Visualisasi Data UTS - Faiq')
st.write('Berikut 5 data teratas dari Southwind.xlsx')
st.write(df.head()) # Cek 5 data teratas

# Soal UTS no 1
st.header('Visualisasi Penjualan per Kategori')
penjualan_kategori = df.groupby('Kategori_produk')['Penjualan'].sum().reset_index()
penjualan_kategori.columns = ['Kategori', 'Total Penjualan']

st.write(penjualan_kategori)
max_value = penjualan_kategori['Total Penjualan'].max()
penjualan_kategori['Highlight'] = penjualan_kategori['Total Penjualan'] == max_value
chart = alt.Chart(penjualan_kategori).mark_bar().encode(
    x='Kategori',
    y='Total Penjualan',
    color=alt.condition(
        alt.datum.Highlight,
        alt.value('green'),   
        alt.value('steelblue') 
    )
)
st.altair_chart(chart)

# Soal UTS no 2
st.header('Visualisasi Penjualan per Wilayah')
penjualan_wilayah = df.groupby('wilayah')['Penjualan'].sum().reset_index()
penjualan_wilayah.columns = ['Wilayah', 'Total Penjualan']

st.write(penjualan_wilayah)
max_value = penjualan_wilayah['Total Penjualan'].max()
penjualan_wilayah['Highlight'] = penjualan_wilayah['Total Penjualan'] == max_value
chart = alt.Chart(penjualan_wilayah).mark_bar().encode(
    x='Wilayah',
    y='Total Penjualan',
    color=alt.condition(
        alt.datum.Highlight,
        alt.value('green'),   
        alt.value('steelblue') 
    )
)
st.altair_chart(chart)

# Soal UTS no 3
st.header('Visualisasi Tren Penjualan per Kategori Produk')

df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df['tanggal_pemesanan'] = pd.to_datetime(df['tanggal_pemesanan'])
df['bulan'] = df['tanggal_pemesanan'].dt.to_period('M').astype(str)

kategori_opsi = st.multiselect(
    "Pilih Kategori Produk",
    options=df['Kategori_produk'].unique(),
    default=df['Kategori_produk'].unique()
)

wilayah_opsi = st.multiselect(
    "Pilih Wilayah",
    options=df['wilayah'].unique(),
    default=df['wilayah'].unique()
)

df_filter = df[
    (df['Kategori_produk'].isin(kategori_opsi)) &
    (df['wilayah'].isin(wilayah_opsi))
]

tren_penjualan = pd.pivot_table(
    df_filter,
    values='Penjualan',
    index='bulan',
    columns='Kategori_produk',
    aggfunc='sum',
    fill_value=0
)

tren_penjualan['Total'] = tren_penjualan.sum(axis=1)
st.write("Pivot Table Penjualan:")
st.dataframe(tren_penjualan)

kategori_cols = tren_penjualan.columns.drop('Total')
st.line_chart(tren_penjualan[kategori_cols])

# Soal UTS no 4
st.header('Visualisasi Segmentasi Pelanggan')

kategori_opsi = st.multiselect(
    "Pilih Kategori Produk",
    options=df['Kategori_produk'].unique(),
    default=df['Kategori_produk'].unique(),
    key="kategori_filter_4"
)

wilayah_opsi = st.multiselect(
    "Pilih Wilayah",
    options=df['wilayah'].unique(),
    default=df['wilayah'].unique(),
    key="wilayah_filter_4"
)

df_filter = df[
    (df['Kategori_produk'].isin(kategori_opsi)) &
    (df['wilayah'].isin(wilayah_opsi))
]

penjualan_segmen = df_filter.groupby('segmen')['Penjualan'].sum().reset_index()

st.write("Data Segmentasi Pelanggan:")
st.write(penjualan_segmen)

total = penjualan_segmen['Penjualan'].sum()
penjualan_segmen['Persentase'] = (penjualan_segmen['Penjualan'] / total) * 100

chart = alt.Chart(penjualan_segmen).mark_arc().encode(
    theta=alt.Theta(field="Penjualan", type="quantitative"),
    color=alt.Color(field="segmen", type="nominal"),
     tooltip=[
        alt.Tooltip('segmen:N', title='Segmen'),
        alt.Tooltip('Penjualan:Q', title='Penjualan'),
        alt.Tooltip('Persentase:Q', title='Persentase', format='.2f')
    ]
)
st.altair_chart(chart, use_container_width=True)

# Soal UTS no 5
st.header('Visualisasi Pengaruh Diskon terhadap Keuntungan')
df_plot = df_filter.copy()
st.write("Data Diskon vs Keuntungan:")
st.write(df_plot[['diskon', 'keuntungan']])

x = df_plot['diskon']
y = df_plot['keuntungan']

slope, intercept = np.polyfit(x, y, 1)
df_line = pd.DataFrame({
    'diskon': x,
    'Keuntungan_pred': slope * x + intercept
})

chart = alt.Chart(df_plot).mark_circle(size=60).encode(
    x=alt.X('diskon:Q', title='Diskon'),
    y=alt.Y('keuntungan:Q', title='Keuntungan'),
    tooltip=['diskon', 'keuntungan']
).properties(
    title='Pengaruh Diskon terhadap Keuntungan'
)

line = alt.Chart(df_line).mark_line(color='red').encode(
    x='diskon:Q',
    y='Keuntungan_pred:Q'
)

st.altair_chart(chart + line, use_container_width=True)

# Soal UTS no 6
st.header('Visualisasi Analisis Penjualan vs Keuntungan')
df_plot = df_filter.copy()
df_plot['Penjualan'] = pd.to_numeric(df_plot['Penjualan'], errors='coerce')
df_plot['keuntungan'] = pd.to_numeric(df_plot['keuntungan'], errors='coerce')
df_plot = df_plot.dropna(subset=['Penjualan', 'keuntungan'])
st.write("Data Penjualan vs Keuntungan:")
st.write(df_plot[['Penjualan', 'keuntungan']])

x = df_plot['Penjualan']
y = df_plot['keuntungan']

slope, intercept = np.polyfit(x, y, 1)
df_line = pd.DataFrame({
    'Penjualan': x,
    'Keuntungan_pred': slope * x + intercept
})

scatter = alt.Chart(df_plot).mark_circle(size=60).encode(
    x=alt.X('Penjualan:Q', title='Penjualan'),
    y=alt.Y('keuntungan:Q', title='Keuntungan'),
    tooltip=['Penjualan', 'keuntungan']
).properties(
    title='Analisis Penjualan vs Keuntungan'
)

line = alt.Chart(df_line).mark_line(color='red').encode(
    x='Penjualan:Q',
    y='Keuntungan_pred:Q'
)

st.altair_chart(scatter + line, use_container_width=True)

# Soal UTS no 7
st.header('Analisis Analisis Subkategori')

kategori_opsi = st.multiselect(
    "Kategori Produk",
    options=df['Kategori_produk'].unique(),
    default=df['Kategori_produk'].unique()
)
wilayah_opsi = st.multiselect(
    "Wilayah",
    options=df['wilayah'].unique(),
    default=df['wilayah'].unique()
)
df_filter = df[
    (df['Kategori_produk'].isin(kategori_opsi)) &
    (df['wilayah'].isin(wilayah_opsi)) 
]

df_plot = df_filter.copy()
subkategori = df_plot.groupby('sub_kategori_produk').agg({
    'Penjualan': 'sum',
    'keuntungan': 'sum'
}).reset_index()
subkategori = subkategori.sort_values('sub_kategori_produk')

st.write("Data Subkategori:")
st.write(subkategori)

bar = alt.Chart(subkategori).mark_bar().encode(
    x=alt.X('sub_kategori_produk:N', sort='-y', title='Subkategori'),
    y=alt.Y('Penjualan:Q', title='Penjualan'),
    tooltip=['sub_kategori_produk', 'Penjualan', 'keuntungan']
)
line = alt.Chart(subkategori).mark_line(color='red', point=True).encode(
    x=alt.X('sub_kategori_produk:N'),
    y=alt.Y('keuntungan:Q', title='Keuntungan')
)
st.altair_chart(bar + line, use_container_width=True)