import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style untuk visualisasi
plt.style.use('default')
sns.set_palette("husl")

# Load data
print("=== LOADING DATA ===")
df = pd.read_csv('data.csv')

print(f"Dataset shape: {df.shape}")
print(f"Total records: {len(df)}")
print("\n=== COLUMN INFORMATION ===")
print(df.columns.tolist())

print("\n=== DATA TYPES ===")
print(df.dtypes)

print("\n=== BASIC STATISTICS ===")
print(df.describe())

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== SAMPLE DATA (First 10 rows) ===")
print(df.head(10))

print("\n=== UNIQUE VALUES PER COLUMN ===")
for col in df.columns:
    unique_count = df[col].nunique()
    print(f"{col}: {unique_count} unique values")
    if unique_count <= 10:
        print(f"  Values: {df[col].unique()}")
    print()

print("\n=== USIA DISTRIBUTION ===")
print(f"Min Usia: {df['Usia'].min()}")
print(f"Max Usia: {df['Usia'].max()}")
print(f"Mean Usia: {df['Usia'].mean():.2f}")
print(f"Median Usia: {df['Usia'].median()}")

# Cek nilai 0 pada usia
zero_age_count = len(df[df['Usia'] == 0])
print(f"Records dengan Usia = 0: {zero_age_count}")

print("\n=== HARGA KELAS DISTRIBUTION ===")
print(df['Harga Kelas'].value_counts().sort_index())

print("\n=== KATEGORI DISTRIBUTION ===")
print(df['Kategori'].value_counts())

print("\n=== DOMISILI DISTRIBUTION (Top 20) ===")
print(df['Domisili'].value_counts().head(20))

print("\n=== NAMA PROGRAM DISTRIBUTION (Top 20) ===")
print(df['Nama Program'].value_counts().head(20))
