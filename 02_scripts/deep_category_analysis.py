import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

print("🔍 DEEP DIVE ANALYSIS - SEMUA KATEGORI & SUB-KATEGORI")
print("🎯 Mengapa Seni/Visual/Crafting tidak muncul sebagai cluster terpisah?")
print("=" * 70)

# Load data
df = pd.read_csv('01_data/data_with_clusters.csv')

print(f"📊 Dataset: {len(df)} customers")
print(f"📅 Analysis date: August 2, 2025")

# ===================================================================
# ANALISIS KATEGORI UTAMA
# ===================================================================

print("\n📈 ANALISIS KATEGORI UTAMA")
print("-" * 50)

kategori_counts = df['Kategori'].value_counts()
print("🏆 DISTRIBUSI KATEGORI:")
for kategori, count in kategori_counts.items():
    percentage = (count/len(df))*100
    print(f"   • {kategori}: {count} customers ({percentage:.1f}%)")

# ===================================================================
# ANALISIS SUB-KATEGORI DETAIL
# ===================================================================

print(f"\n🎨 ANALISIS SUB-KATEGORI 1 (TUJUAN)")
print("-" * 50)

sub1_counts = df['Sub Kategori  1 (Tujuan)'].value_counts()
print("🎯 TOP 15 TUJUAN:")
for i, (sub1, count) in enumerate(sub1_counts.head(15).items(), 1):
    percentage = (count/len(df))*100
    print(f"   {i:2d}. {sub1}: {count} customers ({percentage:.1f}%)")

# ===================================================================
# FOCUS PADA HOBI CATEGORY
# ===================================================================

print(f"\n🎨 DEEP DIVE: KATEGORI HOBI")
print("-" * 50)

hobi_data = df[df['Kategori'] == 'Hobi'].copy()
print(f"📊 Total Hobi customers: {len(hobi_data)} ({len(hobi_data)/len(df)*100:.1f}%)")

if len(hobi_data) > 0:
    print(f"\n🎯 HOBI - SUB-KATEGORI 1 (TUJUAN):")
    hobi_sub1 = hobi_data['Sub Kategori  1 (Tujuan)'].value_counts()
    for sub1, count in hobi_sub1.items():
        percentage = (count/len(hobi_data))*100
        print(f"   • {sub1}: {count} customers ({percentage:.1f}%)")
    
    print(f"\n🎨 HOBI - SUB-KATEGORI 2 (MINAT LAIN):")
    hobi_sub2 = hobi_data['Sub Kategori 2 (Minat lain)'].value_counts()
    for sub2, count in hobi_sub2.head(10).items():
        percentage = (count/len(hobi_data))*100
        print(f"   • {sub2}: {count} customers ({percentage:.1f}%)")

# ===================================================================
# ANALISIS SENI/VISUAL/CRAFTING PATTERNS
# ===================================================================

print(f"\n🎨 ANALISIS PATTERN SENI/VISUAL/CRAFTING")
print("-" * 50)

# Define seni/crafting keywords
seni_keywords = [
    'seni', 'visual', 'craft', 'diy', 'jurnal', 'drawing', 'design', 
    'art', 'kreativ', 'gambar', 'lukis', 'kerajinan', 'handmade',
    'aesthetic', 'photography', 'foto', 'video', 'editing'
]

# Check dalam semua kolom kategori
seni_customers = []

for idx, row in df.iterrows():
    is_seni = False
    
    # Check dalam Kategori
    if pd.notna(row['Kategori']) and any(keyword in str(row['Kategori']).lower() for keyword in seni_keywords):
        is_seni = True
    
    # Check dalam Sub Kategori 1
    if pd.notna(row['Sub Kategori  1 (Tujuan)']) and any(keyword in str(row['Sub Kategori  1 (Tujuan)']).lower() for keyword in seni_keywords):
        is_seni = True
    
    # Check dalam Sub Kategori 2
    if pd.notna(row['Sub Kategori 2 (Minat lain)']) and any(keyword in str(row['Sub Kategori 2 (Minat lain)']).lower() for keyword in seni_keywords):
        is_seni = True
    
    # Check dalam Sub Kategori 3
    if pd.notna(row['Sub Kategori 3 (Minat lain)']) and any(keyword in str(row['Sub Kategori 3 (Minat lain)']).lower() for keyword in seni_keywords):
        is_seni = True
    
    # Check dalam Sub Kategori 4
    if pd.notna(row['Sub Kategori 4 (Minat lain)']) and any(keyword in str(row['Sub Kategori 4 (Minat lain)']).lower() for keyword in seni_keywords):
        is_seni = True
    
    # Check dalam Nama Program
    if pd.notna(row['Nama Program']) and any(keyword in str(row['Nama Program']).lower() for keyword in seni_keywords):
        is_seni = True
    
    if is_seni:
        seni_customers.append(idx)

seni_df = df.loc[seni_customers].copy()
print(f"🎨 TOTAL CUSTOMERS DENGAN INTEREST SENI/VISUAL/CRAFTING: {len(seni_df)}")
print(f"📊 Percentage: {len(seni_df)/len(df)*100:.1f}% dari total customers")

if len(seni_df) > 0:
    print(f"\n🎯 DISTRIBUSI SENI/CRAFTING CUSTOMERS PER CLUSTER:")
    seni_cluster_dist = seni_df['Cluster'].value_counts().sort_index()
    for cluster, count in seni_cluster_dist.items():
        cluster_name = {0: "Penggemar Kuliner", 1: "Orang Tua & Anak", 2: "Kreator Fashion"}[cluster]
        percentage_in_cluster = (count/len(seni_df))*100
        percentage_of_cluster = (count/len(df[df['Cluster']==cluster]))*100
        print(f"   • Cluster {cluster} ({cluster_name}): {count} customers")
        print(f"     - {percentage_in_cluster:.1f}% dari semua seni customers")
        print(f"     - {percentage_of_cluster:.1f}% dari cluster {cluster}")

    print(f"\n🎨 TOP PROGRAMS SENI/CRAFTING:")
    seni_programs = seni_df['Nama Program'].value_counts().head(10)
    for program, count in seni_programs.items():
        percentage = (count/len(seni_df))*100
        print(f"   • {program}: {count} customers ({percentage:.1f}%)")

# ===================================================================
# ANALISIS MENGAPA TIDAK JADI CLUSTER TERPISAH
# ===================================================================

print(f"\n🤔 ANALISIS: MENGAPA SENI/CRAFTING TIDAK JADI CLUSTER TERPISAH?")
print("-" * 60)

# Check demographic overlap dengan existing clusters
if len(seni_df) > 0:
    print(f"\n📊 DEMOGRAPHIC ANALYSIS SENI/CRAFTING:")
    
    # Age analysis
    seni_age_avg = seni_df['Usia_Clean'].mean()
    print(f"   • Average Age: {seni_age_avg:.1f} years")
    
    # Compare dengan existing clusters
    for cluster in [0, 1, 2]:
        cluster_data = df[df['Cluster'] == cluster]
        cluster_name = {0: "Penggemar Kuliner", 1: "Orang Tua & Anak", 2: "Kreator Fashion"}[cluster]
        cluster_age_avg = cluster_data['Usia_Clean'].mean()
        age_diff = abs(seni_age_avg - cluster_age_avg)
        print(f"   • Age similarity with {cluster_name}: {age_diff:.1f} years difference")
    
    # Price analysis
    seni_price_avg = seni_df['Harga Kelas'].mean()
    print(f"\n💰 PRICE ANALYSIS:")
    print(f"   • Average Price: Rp{seni_price_avg:.0f}")
    
    for cluster in [0, 1, 2]:
        cluster_data = df[df['Cluster'] == cluster]
        cluster_name = {0: "Penggemar Kuliner", 1: "Orang Tua & Anak", 2: "Kreator Fashion"}[cluster]
        cluster_price_avg = cluster_data['Harga Kelas'].mean()
        price_diff = abs(seni_price_avg - cluster_price_avg)
        print(f"   • Price similarity with {cluster_name}: Rp{price_diff:.0f} difference")
    
    # Geographic analysis
    print(f"\n🌍 GEOGRAPHIC ANALYSIS:")
    seni_regions = seni_df['Region'].value_counts().head(3)
    print("   • Top regions untuk seni customers:")
    for region, count in seni_regions.items():
        percentage = (count/len(seni_df))*100
        print(f"     - {region}: {count} customers ({percentage:.1f}%)")

# ===================================================================
# RE-CLUSTERING DENGAN FOCUS PADA INTEREST/HOBBY
# ===================================================================

print(f"\n🔄 RE-CLUSTERING ANALYSIS - FOCUS PADA INTEREST PATTERNS")
print("-" * 60)

# Create interest-based features
df_interest = df.copy()

# Create binary features untuk main interests
interest_categories = [
    'kuliner', 'memasak', 'cook', 'makanan', 'food',
    'anak', 'child', 'kid', 'parenting', 'family', 'keluarga',
    'fashion', 'style', 'pakaian', 'outfit', 'trend',
    'seni', 'art', 'kreativ', 'design', 'visual', 'craft', 'diy',
    'teknologi', 'tech', 'digital', 'programming', 'coding',
    'bisnis', 'entrepreneur', 'usaha', 'marketing', 'sales',
    'kesehatan', 'health', 'fitness', 'olahraga', 'sport',
    'pendidikan', 'education', 'belajar', 'learning', 'skill'
]

# Create interest features
for interest in interest_categories:
    df_interest[f'interest_{interest}'] = 0
    
    # Check across all text columns
    text_columns = ['Kategori', 'Sub Kategori  1 (Tujuan)', 'Sub Kategori 2 (Minat lain)', 
                   'Sub Kategori 3 (Minat lain)', 'Sub Kategori 4 (Minat lain)', 'Nama Program']
    
    for col in text_columns:
        if col in df_interest.columns:
            mask = df_interest[col].astype(str).str.lower().str.contains(interest, na=False)
            df_interest.loc[mask, f'interest_{interest}'] = 1

# Count interest patterns
print("🎯 INTEREST PATTERN ANALYSIS:")
for interest in interest_categories:
    count = df_interest[f'interest_{interest}'].sum()
    percentage = (count/len(df_interest))*100
    if count > 0:
        print(f"   • {interest.title()}: {count} customers ({percentage:.1f}%)")

# Check if seni/art forms a natural cluster
seni_interest_customers = df_interest[df_interest['interest_seni'] == 1]
if len(seni_interest_customers) > 50:  # Only if substantial number
    print(f"\n🎨 SENI/ART CLUSTER POTENTIAL:")
    print(f"   • Size: {len(seni_interest_customers)} customers")
    print(f"   • Avg Age: {seni_interest_customers['Usia_Clean'].mean():.1f} years")
    print(f"   • Avg Price: Rp{seni_interest_customers['Harga Kelas'].mean():.0f}")
    print(f"   • Geographic spread: {len(seni_interest_customers['Region'].unique())} regions")

# ===================================================================
# ALTERNATIVE CLUSTERING WITH K=4 or K=5
# ===================================================================

print(f"\n🔄 ALTERNATIVE CLUSTERING - K=4 DAN K=5")
print("-" * 50)

# Prepare features for clustering
feature_columns = ['Usia_Clean', 'Harga Kelas', 'Kategori_encoded', 'Region_encoded', 'Sub1_encoded', 'Sub2_encoded']
available_features = [col for col in feature_columns if col in df.columns]

if len(available_features) >= 4:
    X = df[available_features].fillna(df[available_features].median())
    
    # Try K=4
    kmeans_4 = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['Cluster_K4'] = kmeans_4.fit_predict(X)
    
    # Try K=5  
    kmeans_5 = KMeans(n_clusters=5, random_state=42, n_init=10)
    df['Cluster_K5'] = kmeans_5.fit_predict(X)
    
    print("📊 CLUSTER ANALYSIS K=4:")
    for i in range(4):
        cluster_data = df[df['Cluster_K4'] == i]
        print(f"\n   🎯 Cluster {i}: {len(cluster_data)} customers ({len(cluster_data)/len(df)*100:.1f}%)")
        
        # Top categories in this cluster
        if len(cluster_data) > 0:
            top_category = cluster_data['Kategori'].mode().iloc[0] if len(cluster_data['Kategori'].mode()) > 0 else 'Unknown'
            top_sub1 = cluster_data['Sub Kategori  1 (Tujuan)'].mode().iloc[0] if len(cluster_data['Sub Kategori  1 (Tujuan)'].mode()) > 0 else 'Unknown'
            avg_age = cluster_data['Usia_Clean'].mean()
            avg_price = cluster_data['Harga Kelas'].mean()
            
            print(f"      • Main Category: {top_category}")
            print(f"      • Main Interest: {top_sub1}")
            print(f"      • Avg Age: {avg_age:.1f} years")
            print(f"      • Avg Price: Rp{avg_price:.0f}")
            
            # Check if this cluster captures seni/art
            seni_in_cluster = len([idx for idx in seni_customers if df.loc[idx, 'Cluster_K4'] == i])
            if seni_in_cluster > 0:
                print(f"      • Seni/Art customers: {seni_in_cluster} ({seni_in_cluster/len(cluster_data)*100:.1f}%)")
    
    print(f"\n📊 CLUSTER ANALYSIS K=5:")
    for i in range(5):
        cluster_data = df[df['Cluster_K5'] == i]
        print(f"\n   🎯 Cluster {i}: {len(cluster_data)} customers ({len(cluster_data)/len(df)*100:.1f}%)")
        
        # Top categories in this cluster
        if len(cluster_data) > 0:
            top_category = cluster_data['Kategori'].mode().iloc[0] if len(cluster_data['Kategori'].mode()) > 0 else 'Unknown'
            top_sub1 = cluster_data['Sub Kategori  1 (Tujuan)'].mode().iloc[0] if len(cluster_data['Sub Kategori  1 (Tujuan)'].mode()) > 0 else 'Unknown'
            avg_age = cluster_data['Usia_Clean'].mean()
            avg_price = cluster_data['Harga Kelas'].mean()
            
            print(f"      • Main Category: {top_category}")
            print(f"      • Main Interest: {top_sub1}")
            print(f"      • Avg Age: {avg_age:.1f} years")
            print(f"      • Avg Price: Rp{avg_price:.0f}")
            
            # Check if this cluster captures seni/art
            seni_in_cluster = len([idx for idx in seni_customers if df.loc[idx, 'Cluster_K5'] == i])
            if seni_in_cluster > 0:
                print(f"      • Seni/Art customers: {seni_in_cluster} ({seni_in_cluster/len(cluster_data)*100:.1f}%)")

# ===================================================================
# DETAILED SUB-CATEGORY ANALYSIS
# ===================================================================

print(f"\n📊 DETAILED SUB-CATEGORY ANALYSIS")
print("-" * 50)

print(f"\n🎯 SUB-KATEGORI 2 (MINAT LAIN) - TOP 20:")
sub2_counts = df['Sub Kategori 2 (Minat lain)'].value_counts()
for i, (sub2, count) in enumerate(sub2_counts.head(20).items(), 1):
    percentage = (count/len(df))*100
    print(f"   {i:2d}. {sub2}: {count} customers ({percentage:.1f}%)")

print(f"\n🎯 SUB-KATEGORI 3 (MINAT LAIN) - TOP 15:")
sub3_counts = df['Sub Kategori 3 (Minat lain)'].value_counts()
for i, (sub3, count) in enumerate(sub3_counts.head(15).items(), 1):
    percentage = (count/len(df))*100
    print(f"   {i:2d}. {sub3}: {count} customers ({percentage:.1f}%)")

print(f"\n🎯 SUB-KATEGORI 4 (MINAT LAIN) - TOP 15:")
sub4_counts = df['Sub Kategori 4 (Minat lain)'].value_counts()
for i, (sub4, count) in enumerate(sub4_counts.head(15).items(), 1):
    percentage = (count/len(df))*100
    print(f"   {i:2d}. {sub4}: {count} customers ({percentage:.1f}%)")

# ===================================================================
# CONCLUSION & RECOMMENDATIONS
# ===================================================================

print(f"\n💡 KESIMPULAN & REKOMENDASI")
print("=" * 50)

if len(seni_df) > 0:
    seni_percentage = len(seni_df)/len(df)*100
    print(f"✅ SENI/VISUAL/CRAFTING CUSTOMERS EXISTS: {len(seni_df)} customers ({seni_percentage:.1f}%)")
    
    # Analyze distribution across clusters
    seni_in_cluster = {}
    for cluster in [0, 1, 2]:
        seni_in_cluster[cluster] = len(seni_df[seni_df['Cluster'] == cluster])
    
    dominant_cluster = max(seni_in_cluster, key=seni_in_cluster.get)
    cluster_names = {0: "Penggemar Kuliner", 1: "Orang Tua & Anak", 2: "Kreator Fashion"}
    
    print(f"\n📊 DISTRIBUSI ANALYSIS:")
    print(f"   • Terbanyak di Cluster {dominant_cluster} ({cluster_names[dominant_cluster]}): {seni_in_cluster[dominant_cluster]} customers")
    print(f"   • Tersebar di semua cluster, tidak terisolasi")
    
    if seni_percentage >= 15:
        print(f"\n💡 REKOMENDASI:")
        print(f"   • Seni/Crafting segment CUKUP BESAR untuk dijadikan target bisnis")
        print(f"   • Pertimbangkan K=4 atau K=5 clustering untuk isolasi segment ini")
        print(f"   • Potential business: Kelas seni online, DIY workshops, creative hobbies")
    else:
        print(f"\n💡 REKOMENDASI:")
        print(f"   • Seni/Crafting customers EXISTS tapi terdistribusi across clusters")
        print(f"   • Bisa dijadikan CROSS-SELLING opportunity")
        print(f"   • Focus pada cluster dominan dengan seni interest tambahan")

# Save detailed analysis
if len(seni_df) > 0:
    seni_df.to_csv('05_results/seni_crafting_customers.csv', index=False)
    print(f"\n📁 SAVED: 05_results/seni_crafting_customers.csv")

# Save alternative clustering if performed
if 'Cluster_K4' in df.columns:
    df[['Cluster', 'Cluster_K4', 'Cluster_K5']].to_csv('05_results/alternative_clustering.csv', index=False)
    print(f"📁 SAVED: 05_results/alternative_clustering.csv")

print(f"\n✅ DEEP DIVE ANALYSIS COMPLETE!")
print(f"🎯 KEY FINDING: Seni/Visual/Crafting customers ada {len(seni_df)} orang ({len(seni_df)/len(df)*100:.1f}%)")
print(f"📊 Tersebar across existing clusters - bisa jadi cross-selling opportunity!")
