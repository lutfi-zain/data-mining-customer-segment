"""
🔍 COMPREHENSIVE DATA MINING & CUSTOMER SEGMENTATION ANALYSIS
Complete end-to-end analysis dengan multiple perspectives dan detailed insights
Created: August 2, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.manifold import TSNE
import warnings
warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('default')
sns.set_palette("husl")

print("🔍 COMPREHENSIVE DATA MINING & CUSTOMER SEGMENTATION ANALYSIS")
print("="*80)

# Load and examine data
print("\n📊 STEP 1: DATA LOADING & INITIAL EXPLORATION")
print("-"*50)

df = pd.read_csv('01_data/data.csv')
print(f"Dataset shape: {df.shape}")
print(f"Total customers: {len(df):,}")
print(f"Total features: {df.shape[1]}")

# Display all column names and types
print("\n📋 COMPLETE COLUMN ANALYSIS:")
for i, col in enumerate(df.columns):
    print(f"{i+1:2d}. {col:30s} | Type: {df[col].dtype} | Unique: {df[col].nunique():,}")

# Basic statistics
print("\n📈 BASIC DATASET STATISTICS:")
print(df.describe(include='all'))

print("\n🔍 STEP 2: DETAILED DATA QUALITY ANALYSIS")
print("-"*50)

# Missing values analysis
missing_data = pd.DataFrame({
    'Column': df.columns,
    'Missing_Count': df.isnull().sum(),
    'Missing_Percentage': (df.isnull().sum() / len(df)) * 100,
    'Data_Type': df.dtypes
})
missing_data = missing_data.sort_values('Missing_Percentage', ascending=False)
print("\n🚨 MISSING DATA ANALYSIS:")
print(missing_data)

# Unique values analysis for categorical columns
print("\n📊 CATEGORICAL VARIABLES ANALYSIS:")
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    unique_count = df[col].nunique()
    print(f"\n{col}:")
    print(f"  Unique values: {unique_count}")
    if unique_count <= 20:  # Show values if not too many
        value_counts = df[col].value_counts()
        for val, count in value_counts.items():
            print(f"    {val}: {count} ({count/len(df)*100:.1f}%)")
    else:
        print(f"  Top 10 values:")
        value_counts = df[col].value_counts().head(10)
        for val, count in value_counts.items():
            print(f"    {val}: {count} ({count/len(df)*100:.1f}%)")

print("\n🔍 STEP 3: COMPREHENSIVE DEMOGRAPHIC ANALYSIS")
print("-"*50)

# Age analysis
if 'Umur' in df.columns:
    print("\n👥 AGE DISTRIBUTION ANALYSIS:")
    print(f"Age range: {df['Umur'].min()} - {df['Umur'].max()}")
    print(f"Mean age: {df['Umur'].mean():.1f}")
    print(f"Median age: {df['Umur'].median():.1f}")
    print(f"Standard deviation: {df['Umur'].std():.1f}")
    
    # Age groups
    df['Age_Group'] = pd.cut(df['Umur'], 
                            bins=[0, 18, 25, 35, 45, 55, 100], 
                            labels=['<18', '18-25', '26-35', '36-45', '46-55', '55+'])
    age_dist = df['Age_Group'].value_counts().sort_index()
    print("\nAge Group Distribution:")
    for group, count in age_dist.items():
        print(f"  {group}: {count} ({count/len(df)*100:.1f}%)")

# Price analysis
price_cols = [col for col in df.columns if 'Harga' in col or 'Price' in col]
for col in price_cols:
    if col in df.columns:
        print(f"\n💰 {col.upper()} ANALYSIS:")
        print(f"Range: Rp{df[col].min():,} - Rp{df[col].max():,}")
        print(f"Mean: Rp{df[col].mean():,.0f}")
        print(f"Median: Rp{df[col].median():,.0f}")
        
        # Price segments
        df[f'{col}_Segment'] = pd.cut(df[col], 
                                     bins=5, 
                                     labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
        price_dist = df[f'{col}_Segment'].value_counts()
        print(f"\n{col} Segments:")
        for segment, count in price_dist.items():
            print(f"  {segment}: {count} ({count/len(df)*100:.1f}%)")

# Location analysis
location_cols = [col for col in df.columns if any(x in col.lower() for x in ['lokasi', 'location', 'kota', 'daerah'])]
for col in location_cols:
    if col in df.columns:
        print(f"\n🌍 {col.upper()} ANALYSIS:")
        location_dist = df[col].value_counts()
        print("Top 15 locations:")
        for i, (loc, count) in enumerate(location_dist.head(15).items()):
            print(f"  {i+1:2d}. {loc}: {count} ({count/len(df)*100:.1f}%)")

print("\n🔍 STEP 4: INTEREST & CATEGORY DEEP DIVE ANALYSIS")
print("-"*50)

# Find all interest/category columns
interest_cols = []
for col in df.columns:
    if any(x in col.lower() for x in ['kategori', 'interest', 'hobby', 'minat']):
        interest_cols.append(col)

print(f"Found {len(interest_cols)} interest/category columns:")
for i, col in enumerate(interest_cols):
    print(f"  {i+1}. {col}")

# Analyze each interest column
all_interests = []
interest_analysis = {}

for col in interest_cols:
    print(f"\n📊 {col.upper()} DETAILED ANALYSIS:")
    
    # Get all unique values
    unique_interests = df[col].dropna().unique()
    print(f"Total unique interests: {len(unique_interests)}")
    
    # Count frequency
    interest_counts = df[col].value_counts()
    interest_analysis[col] = interest_counts
    
    print("Top 20 interests:")
    for i, (interest, count) in enumerate(interest_counts.head(20).items()):
        percentage = count/len(df)*100
        print(f"  {i+1:2d}. {interest:40s}: {count:4d} ({percentage:5.1f}%)")
        all_interests.append(interest)
    
    print(f"\nStatistics for {col}:")
    print(f"  Most popular: {interest_counts.index[0]} ({interest_counts.iloc[0]} customers)")
    print(f"  Least popular: {interest_counts.index[-1]} ({interest_counts.iloc[-1]} customers)")
    print(f"  Average per interest: {interest_counts.mean():.1f}")

# Combined interest analysis
print(f"\n🔍 COMBINED INTEREST ANALYSIS:")
print(f"Total unique interests across all categories: {len(set(all_interests))}")

# Create interest matrix for clustering
print("\n🔍 STEP 5: ADVANCED CLUSTERING ANALYSIS")
print("-"*50)

# Prepare numerical data for clustering
numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
print(f"Numerical columns found: {len(numerical_cols)}")
for col in numerical_cols:
    print(f"  - {col}")

# Create clustering dataset
clustering_data = df[numerical_cols].fillna(df[numerical_cols].median())

# Standardize the data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(clustering_data)

print(f"\nClustering dataset shape: {scaled_data.shape}")

# Test multiple clustering algorithms
clustering_results = {}

print("\n🤖 TESTING MULTIPLE CLUSTERING ALGORITHMS:")

# 1. K-Means with different K values
kmeans_scores = {}
k_range = range(2, 11)

print("\n1. K-MEANS CLUSTERING:")
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaled_data)
    
    silhouette = silhouette_score(scaled_data, labels)
    calinski = calinski_harabasz_score(scaled_data, labels)
    davies_bouldin = davies_bouldin_score(scaled_data, labels)
    
    kmeans_scores[k] = {
        'silhouette': silhouette,
        'calinski_harabasz': calinski,
        'davies_bouldin': davies_bouldin,
        'labels': labels
    }
    
    print(f"  K={k}: Silhouette={silhouette:.3f}, Calinski-Harabasz={calinski:.1f}, Davies-Bouldin={davies_bouldin:.3f}")

# Find optimal K
best_k_silhouette = max(kmeans_scores.keys(), key=lambda k: kmeans_scores[k]['silhouette'])
best_k_calinski = max(kmeans_scores.keys(), key=lambda k: kmeans_scores[k]['calinski_harabasz'])
best_k_davies = min(kmeans_scores.keys(), key=lambda k: kmeans_scores[k]['davies_bouldin'])

print(f"\nOptimal K values:")
print(f"  Best K by Silhouette Score: {best_k_silhouette} (score: {kmeans_scores[best_k_silhouette]['silhouette']:.3f})")
print(f"  Best K by Calinski-Harabasz: {best_k_calinski} (score: {kmeans_scores[best_k_calinski]['calinski_harabasz']:.1f})")
print(f"  Best K by Davies-Bouldin: {best_k_davies} (score: {kmeans_scores[best_k_davies]['davies_bouldin']:.3f})")

# 2. DBSCAN Clustering
print("\n2. DBSCAN CLUSTERING:")
eps_values = [0.3, 0.5, 0.7, 1.0, 1.5]
min_samples_values = [5, 10, 15, 20]

dbscan_results = {}
for eps in eps_values:
    for min_samples in min_samples_values:
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        labels = dbscan.fit_predict(scaled_data)
        
        n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = list(labels).count(-1)
        
        if n_clusters > 1:  # Valid clustering
            silhouette = silhouette_score(scaled_data, labels) if n_clusters > 1 else -1
            dbscan_results[f"eps_{eps}_min_{min_samples}"] = {
                'n_clusters': n_clusters,
                'n_noise': n_noise,
                'silhouette': silhouette,
                'labels': labels
            }
            print(f"  eps={eps}, min_samples={min_samples}: {n_clusters} clusters, {n_noise} noise points, Silhouette={silhouette:.3f}")

# 3. Hierarchical Clustering
print("\n3. HIERARCHICAL CLUSTERING:")
hierarchical_scores = {}
for n_clusters in range(2, 8):
    hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
    labels = hierarchical.fit_predict(scaled_data)
    
    silhouette = silhouette_score(scaled_data, labels)
    hierarchical_scores[n_clusters] = {
        'silhouette': silhouette,
        'labels': labels
    }
    print(f"  {n_clusters} clusters: Silhouette={silhouette:.3f}")

print("\n🔍 STEP 6: DETAILED CLUSTER ANALYSIS FOR BEST MODELS")
print("-"*50)

# Analyze the best K-Means model
best_k = best_k_silhouette
best_labels = kmeans_scores[best_k]['labels']
df['Cluster_KMeans'] = best_labels

print(f"\n📊 DETAILED ANALYSIS FOR K-MEANS (K={best_k}):")

# Cluster size distribution
cluster_sizes = pd.Series(best_labels).value_counts().sort_index()
print("\nCluster Size Distribution:")
for cluster, size in cluster_sizes.items():
    print(f"  Cluster {cluster}: {size:,} customers ({size/len(df)*100:.1f}%)")

# Cluster characteristics by numerical features
print(f"\n📈 CLUSTER CHARACTERISTICS (Numerical Features):")
cluster_stats = df.groupby('Cluster_KMeans')[numerical_cols].agg(['mean', 'median', 'std']).round(2)

for cluster in sorted(df['Cluster_KMeans'].unique()):
    print(f"\n--- CLUSTER {cluster} PROFILE ---")
    cluster_data = df[df['Cluster_KMeans'] == cluster]
    
    print(f"Size: {len(cluster_data):,} customers ({len(cluster_data)/len(df)*100:.1f}%)")
    
    # Numerical characteristics
    for col in numerical_cols:
        if col in df.columns:
            mean_val = cluster_data[col].mean()
            median_val = cluster_data[col].median()
            print(f"  {col}: Mean={mean_val:.1f}, Median={median_val:.1f}")
    
    # Categorical characteristics
    for col in categorical_cols:
        if col in df.columns:
            top_category = cluster_data[col].mode().iloc[0] if len(cluster_data[col].mode()) > 0 else "N/A"
            top_count = cluster_data[col].value_counts().iloc[0] if len(cluster_data[col].value_counts()) > 0 else 0
            top_pct = top_count / len(cluster_data) * 100
            print(f"  {col}: Top={top_category} ({top_pct:.1f}%)")

print("\n🔍 STEP 7: CROSS-CATEGORY INTEREST ANALYSIS")
print("-"*50)

# Advanced interest pattern analysis
if len(interest_cols) >= 2:
    print("\n🔍 CROSS-CATEGORY INTEREST PATTERNS:")
    
    # Create interest co-occurrence matrix
    for i, col1 in enumerate(interest_cols):
        for j, col2 in enumerate(interest_cols[i+1:], i+1):
            print(f"\n{col1} vs {col2} Analysis:")
            
            # Find customers with interests in both categories
            df_interests = df[[col1, col2]].dropna()
            
            if len(df_interests) > 0:
                # Cross-tabulation
                crosstab = pd.crosstab(df_interests[col1], df_interests[col2])
                
                print(f"  Common combinations (Top 10):")
                # Find most common combinations
                combinations = []
                for idx1, row in crosstab.iterrows():
                    for idx2, count in row.items():
                        if count > 0:
                            combinations.append((idx1, idx2, count))
                
                combinations.sort(key=lambda x: x[2], reverse=True)
                for k, (int1, int2, count) in enumerate(combinations[:10]):
                    print(f"    {k+1:2d}. {int1} + {int2}: {count} customers")

print("\n🔍 STEP 8: ADVANCED SEGMENTATION INSIGHTS")
print("-"*50)

# PCA Analysis
print("\n📊 PRINCIPAL COMPONENT ANALYSIS:")
pca = PCA()
pca_data = pca.fit_transform(scaled_data)

# Explained variance
explained_variance = pca.explained_variance_ratio_
cumulative_variance = np.cumsum(explained_variance)

print("Explained Variance by Component:")
for i, (var, cum_var) in enumerate(zip(explained_variance[:10], cumulative_variance[:10])):
    print(f"  PC{i+1}: {var:.3f} ({var*100:.1f}%) | Cumulative: {cum_var:.3f} ({cum_var*100:.1f}%)")

# Find number of components for 80% variance
n_components_80 = np.argmax(cumulative_variance >= 0.8) + 1
print(f"\nComponents needed for 80% variance: {n_components_80}")
print(f"Components needed for 90% variance: {np.argmax(cumulative_variance >= 0.9) + 1}")

# Feature importance in PCA
print(f"\n📈 FEATURE IMPORTANCE IN FIRST {min(len(explained_variance), 3)} COMPONENTS:")
feature_names = numerical_cols
n_components_to_show = min(len(explained_variance), 3)
components_df = pd.DataFrame(
    pca.components_[:n_components_to_show].T,
    columns=[f'PC{i+1}' for i in range(n_components_to_show)],
    index=feature_names
)

for i in range(n_components_to_show):
    pc_name = f'PC{i+1}'
    print(f"\n{pc_name} (explains {explained_variance[i]*100:.1f}% variance):")
    pc_importance = components_df[pc_name].abs().sort_values(ascending=False)
    for feature, importance in pc_importance.items():
        direction = "+" if components_df.loc[feature, pc_name] > 0 else "-"
        print(f"  {direction} {feature}: {abs(importance):.3f}")

print("\n🔍 STEP 9: MARKET SEGMENTATION SUMMARY")
print("-"*50)

# Create comprehensive segmentation summary
print("\n📊 COMPREHENSIVE CUSTOMER SEGMENTATION SUMMARY:")

# Overall dataset characteristics
print(f"\nDATASET OVERVIEW:")
print(f"  Total Customers: {len(df):,}")
print(f"  Data Dimensions: {df.shape[1]} features")
print(f"  Numerical Features: {len(numerical_cols)}")
print(f"  Categorical Features: {len(categorical_cols)}")
print(f"  Interest Categories: {len(interest_cols)}")

# Clustering summary
print(f"\nCLUSTERING RESULTS SUMMARY:")
print(f"  Recommended Clusters (K-Means): {best_k}")
print(f"  Best Silhouette Score: {kmeans_scores[best_k]['silhouette']:.3f}")
print(f"  Alternative Methods Tested: K-Means, DBSCAN, Hierarchical")

# Demographic summary
if 'Umur' in df.columns:
    print(f"\nDEMOGRAPHIC INSIGHTS:")
    print(f"  Age Range: {df['Umur'].min()}-{df['Umur'].max()} years")
    print(f"  Average Age: {df['Umur'].mean():.1f} years")
    print(f"  Age Groups: {df['Age_Group'].nunique()} distinct segments")

# Interest summary
print(f"\nINTEREST ANALYSIS SUMMARY:")
total_unique_interests = len(set(all_interests))
print(f"  Total Unique Interests: {total_unique_interests}")
print(f"  Interest Categories Analyzed: {len(interest_cols)}")

for col in interest_cols:
    if col in interest_analysis:
        top_interest = interest_analysis[col].index[0]
        top_count = interest_analysis[col].iloc[0]
        print(f"  {col}: Top interest is '{top_interest}' ({top_count} customers)")

print("\n✅ COMPREHENSIVE DATA MINING ANALYSIS COMPLETED!")
print("="*80)
print("📊 All analysis results will be used for detailed reporting...")
