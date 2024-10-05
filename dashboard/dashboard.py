import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

dataset = pd.read_csv('dashboard/all_data.csv')
order_data = pd.read_csv('dashboard/all_data_2.csv')

def revenueGroupByCategory(sort):
    dataframe = dataset.groupby('product_category_name_english').agg({
        "order_id": "nunique",
        "price": ["sum", "min", "max", "mean"]
    })
    dataframe.columns = ['order_count', 'total_price', 'min_price', 'max_price', 'mean_price']
    if sort == 'count':
        return dataframe.sort_values(by='order_count', ascending=False).head(10)
    else:
        return 'wrong parameter'
  
def revenueGroupMonth(sort):
    monthly_orders = order_data.groupby('purchase_month').agg({
    "order_id": "nunique",   
    })
    if sort == 'count':
        monthly_orders.columns = ['order_count']
        return monthly_orders.sort_values(by="order_count", ascending=False).head(10)
    else: 
        return 'wrong parameter'


st.title('e-Commerce Performance')

tabProduct, tabMonth, tabConclusion = st.tabs(['Product', 'Month', 'Conclusion'])

with tabProduct:
    st.header('Penjualan Kategori Produk Paling Tertinggi (Top 10)')
    st.subheader('Jumlah Pesanan per Kategori Produk')
    
    product_category = revenueGroupByCategory('count')
    
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(x=product_category.index, y=product_category['order_count'],color='skyblue', ax=ax)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_title('Jumlah Pesanan per Kategori Produk')
    ax.set_xlabel('Kategori Produk')
    ax.set_ylabel('Jumlah Pesanan')
    st.pyplot(fig)
    top_category = product_category.index[0]
    top_order = product_category.iloc[0]['order_count']
    st.write(f"Kategori produk dengan jumlah pesanan tertinggi adalah **{top_category}** dengan total {top_order} pesanan.")

# Month Analysis
with tabMonth:
    st.header('Waktu Pembelian Terbanyak(Bulan)')
    
    top = revenueGroupMonth('count')
    
    st.subheader('Jumlah Pembelian per Bulan')
    
    fig, ax = plt.subplots(figsize=(10,6))
    top.plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title('Jumlah Pembelian per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pembelian')
    plt.xticks(rotation=45)
    
    st.pyplot(fig)
    top_month = top.index[0]
    top_orderM = top.iloc[0]['order_count']
    st.write(f"Bulan yang menjadi puncak waktu pembelian adalah **{top_month}**/bulan November 2017 dengan jumlah pembelian sebanyak **{top_orderM}** pembelian")

with tabConclusion:
    st.header('Kesimpulan/Conclusion')
    st.subheader('Pertanyaan 1 : Kategori Produk mana yang memiliki penjualan tertinggi?')
    st.write(f"Kategori product yang memiliki penjualan tertinggi adalah bed bath table dengan terjual sebanyak 9417 pesanan")

    st.subheader('Kapan puncak waktu pembelian terjadi (bulan)?')
    st.write(f"yang menjadi puncak waktu pembelian dalam bulan adalah bulan ke-11 atau november tahun 2017 dengan jumlah pembelian sebanyak 7544 pembelian")
