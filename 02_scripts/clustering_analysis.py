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
df = pd.read_csv('data_with_segments.csv')

print("=== MACHINE LEARNING CLUSTERING ANALYSIS ===")

# Prepare data for clustering
# Select features for clustering
features_for_clustering = ['Usia', 'Harga Kelas']

# Handle missing values (Usia = 0)
df_ml = df.copy()
df_ml['Usia'] = df_ml['Usia'].replace(0, df_ml['Usia'].median())

# Encode categorical variables
le_kategori = LabelEncoder()
le_region = LabelEncoder()
le_sub1 = LabelEncoder()
le_sub2 = LabelEncoder()

df_ml['Kategori_encoded'] = le_kategori.fit_transform(df_ml['Kategori'])
df_ml['Region_encoded'] = le_region.fit_transform(df_ml['Region'])
df_ml['Sub1_encoded'] = le_sub1.fit_transform(df_ml['Sub Kategori  1 (Tujuan)'])
df_ml['Sub2_encoded'] = le_sub2.fit_transform(df_ml['Sub Kategori 2 (Minat lain)'])

# Features for clustering
X = df_ml[['Usia', 'Harga Kelas', 'Kategori_encoded', 'Region_encoded', 'Sub1_encoded', 'Sub2_encoded']]

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Find optimal number of clusters using elbow method
print("=== FINDING OPTIMAL NUMBER OF CLUSTERS ===")
inertias = []
silhouette_scores = []
k_range = range(2, 11)

for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(X_scaled)
    inertias.append(kmeans.inertia_)
    sil_score = silhouette_score(X_scaled, kmeans.labels_)
    silhouette_scores.append(sil_score)
    print(f"K={k}: Inertia={kmeans.inertia_:.2f}, Silhouette={sil_score:.3f}")

# Choose optimal k (highest silhouette score)
optimal_k = k_range[np.argmax(silhouette_scores)]
print(f"\nOptimal number of clusters: {optimal_k}")

# Perform final clustering
kmeans_final = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
df_ml['Cluster'] = kmeans_final.fit_predict(X_scaled)

print(f"\n=== CLUSTER ANALYSIS (K={optimal_k}) ===")

# Analyze each cluster
for cluster_id in sorted(df_ml['Cluster'].unique()):
    cluster_data = df_ml[df_ml['Cluster'] == cluster_id]
    print(f"\n--- CLUSTER {cluster_id} ({len(cluster_data)} customers, {len(cluster_data)/len(df_ml)*100:.1f}%) ---")
    
    print(f"Usia: Mean={cluster_data['Usia'].mean():.1f}, Median={cluster_data['Usia'].median():.1f}")
    print(f"Harga: Mean={cluster_data['Harga Kelas'].mean():.1f}, Median={cluster_data['Harga Kelas'].median():.1f}")
    
    print("Top 3 Kategori:")
    print(cluster_data['Kategori'].value_counts().head(3))
    
    print("Top 3 Region:")
    print(cluster_data['Region'].value_counts().head(3))
    
    print("Top 3 Age Groups:")
    print(cluster_data['Age_Group'].value_counts().head(3))
    
    print("Top 3 Price Segments:")
    print(cluster_data['Price_Segment'].value_counts().head(3))

# Create customer personas
print(f"\n=== CUSTOMER PERSONAS ===")

personas = {}
for cluster_id in sorted(df_ml['Cluster'].unique()):
    cluster_data = df_ml[df_ml['Cluster'] == cluster_id]
    
    # Most common characteristics
    top_category = cluster_data['Kategori'].mode()[0]
    top_age_group = cluster_data['Age_Group'].mode()[0]
    top_price_segment = cluster_data['Price_Segment'].mode()[0]
    top_region = cluster_data['Region'].mode()[0]
    avg_age = cluster_data['Usia'].mean()
    avg_price = cluster_data['Harga Kelas'].mean()
    
    # Create persona name
    if 'Anak' in top_category or 'Anak' in top_age_group:
        persona_name = "Parents & Kids Segment"
    elif 'Memasak' in top_category:
        persona_name = "Cooking Enthusiasts"
    elif 'Hobi' in top_category:
        persona_name = "Hobby Learners"
    elif 'Fashion' in top_category:
        persona_name = "Fashion Creators"
    elif avg_price > 80:
        persona_name = "Premium Learners"
    else:
        persona_name = f"General Segment {cluster_id}"
    
    personas[cluster_id] = {
        'name': persona_name,
        'size': len(cluster_data),
        'percentage': len(cluster_data)/len(df_ml)*100,
        'avg_age': avg_age,
        'avg_price': avg_price,
        'top_category': top_category,
        'top_age_group': top_age_group,
        'top_price_segment': top_price_segment,
        'top_region': top_region
    }

for cluster_id, persona in personas.items():
    print(f"\n🎯 CLUSTER {cluster_id}: {persona['name']}")
    print(f"   📊 Size: {persona['size']:,} customers ({persona['percentage']:.1f}%)")
    print(f"   👤 Profile: {persona['top_age_group']}, Avg Age: {persona['avg_age']:.1f}")
    print(f"   💰 Spending: {persona['top_price_segment']}, Avg: Rp{persona['avg_price']:.0f}k")
    print(f"   📚 Interest: {persona['top_category']}")
    print(f"   📍 Location: {persona['top_region']}")

# Save results
df_ml.to_csv('data_with_clusters.csv', index=False)

print(f"\n=== BUSINESS INSIGHTS & RECOMMENDATIONS ===")
print("Berdasarkan analisis clustering, berikut insights utama:")

# Count clusters by main characteristics
category_clusters = df_ml.groupby(['Cluster', 'Kategori']).size().unstack(fill_value=0)
print("\n1. DISTRIBUSI KATEGORI PER CLUSTER:")
print(category_clusters)

price_clusters = df_ml.groupby(['Cluster', 'Price_Segment']).size().unstack(fill_value=0)
print("\n2. DISTRIBUSI HARGA PER CLUSTER:")
print(price_clusters)

print(f"\n✅ File hasil clustering: 'data_with_clusters.csv'")
print(f"✅ Total clusters ditemukan: {optimal_k}")
print(f"✅ Silhouette Score: {max(silhouette_scores):.3f}")

# Marketing recommendations
print(f"\n=== MARKETING STRATEGY RECOMMENDATIONS ===")
for cluster_id, persona in personas.items():
    print(f"\n🎯 {persona['name']} (Cluster {cluster_id}):")
    
    if 'Anak' in persona['name'] or 'Parents' in persona['name']:
        print("   📢 Focus on parenting communities, educational content")
        print("   💡 Bundle packages for multiple children")
        print("   📱 Target social media where parents are active")
    
    elif 'Cooking' in persona['name']:
        print("   📢 Partner with food bloggers and culinary influencers")
        print("   💡 Offer advanced cooking classes and chef certifications")
        print("   📱 Create recipe-sharing community")
    
    elif 'Fashion' in persona['name']:
        print("   📢 Collaborate with fashion designers and boutiques")
        print("   💡 Focus on business/entrepreneurship aspects")
        print("   📱 Instagram and Pinterest marketing")
    
    elif 'Premium' in persona['name']:
        print("   📢 Emphasize quality, exclusivity, and personal attention")
        print("   💡 Offer VIP services and advanced certifications")
        print("   📱 LinkedIn and professional networks")
    
    else:
        print("   📢 General digital marketing across platforms")
        print("   💡 Diverse course offerings and flexible pricing")
        print("   📱 Facebook and WhatsApp engagement")
