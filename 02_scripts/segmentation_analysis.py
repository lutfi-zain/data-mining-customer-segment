import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_csv('data.csv')

print("=== CUSTOMER SEGMENTATION ANALYSIS ===")
print("Berdasarkan data yang ada, kita akan melakukan segmentasi customer menggunakan beberapa pendekatan:")
print("1. Segmentasi berdasarkan Demografi (Usia & Lokasi)")
print("2. Segmentasi berdasarkan Behavior (Kategori program & Harga)")
print("3. Segmentasi berdasarkan Interest (Sub-kategori minat)")
print("4. Clustering menggunakan Machine Learning")

# Data Cleaning
print("\n=== DATA CLEANING ===")
# Handle usia = 0 (kemungkinan data untuk anak yang diisi orang tua)
df_clean = df.copy()
df_clean['Usia_Clean'] = df_clean['Usia'].replace(0, np.nan)

print(f"Records dengan Usia = 0: {(df['Usia'] == 0).sum()}")
print("Catatan: Usia = 0 kemungkinan adalah data anak yang didaftarkan orang tua")

# 1. SEGMENTASI DEMOGRAFIS
print("\n=== 1. SEGMENTASI DEMOGRAFIS ===")

# Age Groups
def categorize_age(age):
    if pd.isna(age) or age == 0:
        return 'Anak/Tidak Diketahui'
    elif age <= 12:
        return 'Anak (≤12)'
    elif age <= 17:
        return 'Remaja (13-17)'
    elif age <= 25:
        return 'Dewasa Muda (18-25)'
    elif age <= 35:
        return 'Dewasa (26-35)'
    elif age <= 45:
        return 'Dewasa Menengah (36-45)'
    else:
        return 'Dewasa Tua (>45)'

df_clean['Age_Group'] = df_clean['Usia'].apply(categorize_age)
print("Distribusi Kelompok Usia:")
print(df_clean['Age_Group'].value_counts())

# Regional Segmentation
def categorize_region(domisili):
    jakarta_area = ['jakarta', 'bekasi', 'depok', 'tangerang', 'bogor']
    jatim = ['surabaya', 'malang', 'sidoarjo', 'jember', 'mojokerto', 'tuban', 'lamongan', 'ngawi']
    jateng = ['semarang', 'magelang', 'sukoharjo', 'cilacap', 'purbalingga', 'temanggung', 'karanganyar', 'wonogiri']
    
    domisili_lower = domisili.lower()
    
    if any(area in domisili_lower for area in jakarta_area):
        return 'Jabodetabek'
    elif any(area in domisili_lower for area in jatim):
        return 'Jawa Timur'
    elif any(area in domisili_lower for area in jateng):
        return 'Jawa Tengah'
    elif 'bandung' in domisili_lower or 'garut' in domisili_lower or 'kuningan' in domisili_lower:
        return 'Jawa Barat'
    elif 'yogya' in domisili_lower or 'bantul' in domisili_lower:
        return 'DIY'
    elif any(kota in domisili_lower for kota in ['ambon', 'luhu']):
        return 'Maluku'
    elif any(kota in domisili_lower for kota in ['balikpapan', 'samarinda', 'kaltim']):
        return 'Kalimantan Timur'
    elif 'makassar' in domisili_lower or 'kendari' in domisili_lower:
        return 'Sulawesi'
    else:
        return 'Lainnya'

df_clean['Region'] = df_clean['Domisili'].apply(categorize_region)
print("\nDistribusi Regional:")
print(df_clean['Region'].value_counts())

# 2. SEGMENTASI BEHAVIORAL
print("\n=== 2. SEGMENTASI BEHAVIORAL ===")

# Price Segmentation
def categorize_price(price):
    if price <= 30:
        return 'Budget (≤30k)'
    elif price <= 65:
        return 'Standard (31-65k)'
    elif price <= 100:
        return 'Premium (66-100k)'
    else:
        return 'Luxury (>100k)'

df_clean['Price_Segment'] = df_clean['Harga Kelas'].apply(categorize_price)
print("Distribusi Segmen Harga:")
print(df_clean['Price_Segment'].value_counts())

print("\nDistribusi Kategori Program:")
print(df_clean['Kategori'].value_counts())

# 3. SEGMENTASI BERDASARKAN MINAT
print("\n=== 3. SEGMENTASI BERDASARKAN MINAT ===")

print("Sub Kategori 1 (Tujuan):")
print(df_clean['Sub Kategori  1 (Tujuan)'].value_counts())

print("\nSub Kategori 2 (Minat lain):")
print(df_clean['Sub Kategori 2 (Minat lain)'].value_counts())

# Cross-tabulation untuk insight lebih dalam
print("\n=== CROSS-TABULATION ANALYSIS ===")

print("1. Age Group vs Kategori:")
ct_age_category = pd.crosstab(df_clean['Age_Group'], df_clean['Kategori'])
print(ct_age_category)

print("\n2. Price Segment vs Kategori:")
ct_price_category = pd.crosstab(df_clean['Price_Segment'], df_clean['Kategori'])
print(ct_price_category)

print("\n3. Region vs Kategori (Top regions):")
top_regions = df_clean['Region'].value_counts().head(5).index
df_top_regions = df_clean[df_clean['Region'].isin(top_regions)]
ct_region_category = pd.crosstab(df_top_regions['Region'], df_top_regions['Kategori'])
print(ct_region_category)

# Save results
df_clean.to_csv('data_with_segments.csv', index=False)
print(f"\n=== SUMMARY ===")
print(f"Data sudah dibersihkan dan disegmentasi!")
print(f"File hasil: 'data_with_segments.csv'")
print(f"Total segments yang dibuat:")
print(f"- Age Groups: {df_clean['Age_Group'].nunique()}")
print(f"- Regions: {df_clean['Region'].nunique()}")
print(f"- Price Segments: {df_clean['Price_Segment'].nunique()}")
print(f"- Categories: {df_clean['Kategori'].nunique()}")
