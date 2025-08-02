import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = [12, 8]

# Load data with clusters
df = pd.read_csv('data_with_clusters.csv')

print("=== CREATING VISUALIZATIONS FOR CUSTOMER SEGMENTS ===")

# 1. Cluster Distribution
plt.figure(figsize=(15, 10))

# Subplot 1: Cluster sizes
plt.subplot(2, 3, 1)
cluster_counts = df['Cluster'].value_counts().sort_index()
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
plt.pie(cluster_counts.values, labels=[f'Cluster {i}\n({count:,} customers)' for i, count in cluster_counts.items()], 
        autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Distribution of Customer Clusters', fontsize=14, fontweight='bold')

# Subplot 2: Age distribution by cluster
plt.subplot(2, 3, 2)
df_no_zero_age = df[df['Usia'] > 0]  # Remove age = 0 for better visualization
sns.boxplot(data=df_no_zero_age, x='Cluster', y='Usia', palette=colors)
plt.title('Age Distribution by Cluster', fontsize=14, fontweight='bold')
plt.xlabel('Cluster')
plt.ylabel('Age')

# Subplot 3: Price distribution by cluster
plt.subplot(2, 3, 3)
sns.boxplot(data=df, x='Cluster', y='Harga Kelas', palette=colors)
plt.title('Price Distribution by Cluster', fontsize=14, fontweight='bold')
plt.xlabel('Cluster')
plt.ylabel('Price (in thousands)')

# Subplot 4: Category distribution by cluster
plt.subplot(2, 3, 4)
category_cluster = pd.crosstab(df['Cluster'], df['Kategori'])
category_cluster_pct = category_cluster.div(category_cluster.sum(axis=1), axis=0) * 100
sns.heatmap(category_cluster_pct, annot=True, fmt='.1f', cmap='YlOrRd', cbar_kws={'label': 'Percentage'})
plt.title('Category Distribution by Cluster (%)', fontsize=14, fontweight='bold')
plt.xlabel('Category')
plt.ylabel('Cluster')

# Subplot 5: Price segment by cluster
plt.subplot(2, 3, 5)
price_cluster = pd.crosstab(df['Cluster'], df['Price_Segment'])
price_cluster_pct = price_cluster.div(price_cluster.sum(axis=1), axis=0) * 100
sns.heatmap(price_cluster_pct, annot=True, fmt='.1f', cmap='Blues', cbar_kws={'label': 'Percentage'})
plt.title('Price Segment by Cluster (%)', fontsize=14, fontweight='bold')
plt.xlabel('Price Segment')
plt.ylabel('Cluster')
plt.xticks(rotation=45)

# Subplot 6: Regional distribution by cluster
plt.subplot(2, 3, 6)
region_cluster = pd.crosstab(df['Cluster'], df['Region'])
region_cluster_pct = region_cluster.div(region_cluster.sum(axis=1), axis=0) * 100
# Show only top 5 regions for clarity
top_regions = region_cluster.sum().nlargest(5).index
region_cluster_top = region_cluster_pct[top_regions]
sns.heatmap(region_cluster_top, annot=True, fmt='.1f', cmap='Greens', cbar_kws={'label': 'Percentage'})
plt.title('Top 5 Regions by Cluster (%)', fontsize=14, fontweight='bold')
plt.xlabel('Region')
plt.ylabel('Cluster')
plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('customer_segments_overview.png', dpi=300, bbox_inches='tight')
plt.show()

# 2. Detailed analysis per cluster
for cluster_id in sorted(df['Cluster'].unique()):
    plt.figure(figsize=(15, 10))
    cluster_data = df[df['Cluster'] == cluster_id]
    
    # Determine cluster name
    if cluster_id == 0:
        cluster_name = "Parents & Kids Segment"
        color = colors[0]
    elif cluster_id == 1:
        cluster_name = "Cooking Enthusiasts"
        color = colors[1]
    else:
        cluster_name = "Fashion Creators"
        color = colors[2]
    
    plt.suptitle(f'Cluster {cluster_id}: {cluster_name} ({len(cluster_data):,} customers)', 
                 fontsize=16, fontweight='bold')
    
    # Age distribution
    plt.subplot(2, 3, 1)
    cluster_data_no_zero = cluster_data[cluster_data['Usia'] > 0]
    plt.hist(cluster_data_no_zero['Usia'], bins=15, color=color, alpha=0.7, edgecolor='black')
    plt.title('Age Distribution')
    plt.xlabel('Age')
    plt.ylabel('Count')
    
    # Price distribution
    plt.subplot(2, 3, 2)
    plt.hist(cluster_data['Harga Kelas'], bins=15, color=color, alpha=0.7, edgecolor='black')
    plt.title('Price Distribution')
    plt.xlabel('Price (thousands)')
    plt.ylabel('Count')
    
    # Top categories
    plt.subplot(2, 3, 3)
    top_categories = cluster_data['Kategori'].value_counts().head(5)
    plt.barh(range(len(top_categories)), top_categories.values, color=color, alpha=0.7)
    plt.yticks(range(len(top_categories)), top_categories.index)
    plt.title('Top Categories')
    plt.xlabel('Count')
    
    # Top regions
    plt.subplot(2, 3, 4)
    top_regions = cluster_data['Region'].value_counts().head(5)
    plt.barh(range(len(top_regions)), top_regions.values, color=color, alpha=0.7)
    plt.yticks(range(len(top_regions)), top_regions.index)
    plt.title('Top Regions')
    plt.xlabel('Count')
    
    # Age groups
    plt.subplot(2, 3, 5)
    age_groups = cluster_data['Age_Group'].value_counts()
    plt.pie(age_groups.values, labels=age_groups.index, autopct='%1.1f%%', 
            colors=sns.color_palette("husl", len(age_groups)))
    plt.title('Age Groups Distribution')
    
    # Price segments
    plt.subplot(2, 3, 6)
    price_segments = cluster_data['Price_Segment'].value_counts()
    plt.pie(price_segments.values, labels=price_segments.index, autopct='%1.1f%%',
            colors=sns.color_palette("viridis", len(price_segments)))
    plt.title('Price Segments Distribution')
    
    plt.tight_layout()
    plt.savefig(f'cluster_{cluster_id}_{cluster_name.replace(" ", "_").replace("&", "and")}.png', 
                dpi=300, bbox_inches='tight')
    plt.show()

# 3. PCA Visualization
print("\n=== PCA VISUALIZATION ===")
from sklearn.preprocessing import StandardScaler

# Prepare data for PCA
df_pca = df.copy()
df_pca['Usia'] = df_pca['Usia'].replace(0, df_pca['Usia'].median())

# Encode categorical variables for PCA
from sklearn.preprocessing import LabelEncoder
le_kategori = LabelEncoder()
le_region = LabelEncoder()

df_pca['Kategori_encoded'] = le_kategori.fit_transform(df_pca['Kategori'])
df_pca['Region_encoded'] = le_region.fit_transform(df_pca['Region'])

# Select features for PCA
features = ['Usia', 'Harga Kelas', 'Kategori_encoded', 'Region_encoded']
X = df_pca[features]

# Scale and apply PCA
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# Plot PCA
plt.figure(figsize=(12, 8))
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df_pca['Cluster'], 
                     cmap='viridis', alpha=0.6, s=50)
plt.colorbar(scatter, label='Cluster')
plt.xlabel(f'First Principal Component (explains {pca.explained_variance_ratio_[0]:.1%} variance)')
plt.ylabel(f'Second Principal Component (explains {pca.explained_variance_ratio_[1]:.1%} variance)')
plt.title('Customer Segments in PCA Space')

# Add cluster centers
for i in range(3):
    cluster_points = X_pca[df_pca['Cluster'] == i]
    center_x = np.mean(cluster_points[:, 0])
    center_y = np.mean(cluster_points[:, 1])
    plt.scatter(center_x, center_y, c='red', s=300, alpha=0.8, marker='x', linewidths=3)
    plt.annotate(f'Cluster {i}', (center_x, center_y), xytext=(5, 5), 
                textcoords='offset points', fontsize=12, fontweight='bold')

plt.grid(True, alpha=0.3)
plt.savefig('pca_clusters.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"📊 Visualizations saved:")
print(f"   - customer_segments_overview.png")
print(f"   - cluster_0_Parents_and_Kids_Segment.png")
print(f"   - cluster_1_Cooking_Enthusiasts.png")
print(f"   - cluster_2_Fashion_Creators.png")
print(f"   - pca_clusters.png")

# Summary Statistics Table
print(f"\n=== CLUSTER SUMMARY TABLE ===")
summary_stats = []

for cluster_id in sorted(df['Cluster'].unique()):
    cluster_data = df[df['Cluster'] == cluster_id]
    
    stats = {
        'Cluster': cluster_id,
        'Name': ['Parents & Kids', 'Cooking Enthusiasts', 'Fashion Creators'][cluster_id],
        'Size': len(cluster_data),
        'Percentage': f"{len(cluster_data)/len(df)*100:.1f}%",
        'Avg_Age': f"{cluster_data['Usia'].mean():.1f}",
        'Avg_Price': f"Rp{cluster_data['Harga Kelas'].mean():.0f}k",
        'Top_Category': cluster_data['Kategori'].mode()[0],
        'Top_Region': cluster_data['Region'].mode()[0]
    }
    summary_stats.append(stats)

summary_df = pd.DataFrame(summary_stats)
print(summary_df.to_string(index=False))

# Save summary
summary_df.to_csv('cluster_summary.csv', index=False)
print(f"\n✅ Cluster summary saved to: cluster_summary.csv")
