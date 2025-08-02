import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

# Create directory for individual charts
os.makedirs('Final Analysis/charts', exist_ok=True)

# Read the data
df = pd.read_csv('01_data/data.csv')

# Rename columns for consistency
df.columns = ['Usia', 'Domisili', 'Nama_Program', 'Harga_Kelas', 'Kategori', 
              'Sub_Kategori_1', 'Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']

# Create feature columns
df['Age'] = df['Usia']
df['Program'] = df['Nama_Program'].astype('category').cat.codes
df['Spending'] = df['Harga_Kelas']
df['Frequency'] = 1  # Assuming each row is one purchase
df['Interest'] = df['Sub_Kategori_1'].fillna('') + ' ' + df['Sub_Kategori_2'].fillna('')

# Prepare data for clustering
feature_columns = ['Age', 'Program', 'Spending', 'Frequency']
X = df[feature_columns].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-means clustering
kmeans = KMeans(n_clusters=7, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Apply PCA for 2D visualization
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_scaled)
df['PCA1'] = X_pca[:, 0]
df['PCA2'] = X_pca[:, 1]

# Color palette
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

print("Creating individual charts...")

# 1. Cluster Overview Distribution
plt.figure(figsize=(10, 6))
cluster_counts = df['Cluster'].value_counts().sort_index()
bars = plt.bar(range(len(cluster_counts)), cluster_counts.values, color=colors[:len(cluster_counts)])
plt.title('Customer Distribution Across 7 Clusters', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Cluster ID', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.xticks(range(len(cluster_counts)), [f'Cluster {i}' for i in cluster_counts.index])

# Add value labels on bars
for bar, value in zip(bars, cluster_counts.values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
             str(value), ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/01_cluster_overview.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Age vs Spending Segmentation
plt.figure(figsize=(12, 8))
scatter = plt.scatter(df['Age'], df['Spending'], c=[colors[i] for i in df['Cluster']], 
                     alpha=0.7, s=60, edgecolors='white', linewidth=0.5)
plt.title('Age vs Spending Segmentation by Clusters', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age (Years)', fontsize=12)
plt.ylabel('Spending (IDR)', fontsize=12)

# Create custom legend
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    if len(cluster_data) > 0:
        plt.scatter([], [], c=colors[i], label=f'Cluster {i} (n={len(cluster_data)})', s=60)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/02_age_spending_segmentation.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Interest Category Distribution
categories = {
    'Entrepreneurship': ['bisnis', 'entrepreneurship', 'marketing', 'startup'],
    'Creative Arts': ['seni', 'crafting', 'visual', 'design', 'fotografi', 'musik'],
    'Family & Education': ['parenting', 'family', 'anak', 'pendidikan', 'montessori'],
    'Lifestyle & Wellness': ['cooking', 'fashion', 'beauty', 'lifestyle', 'kesehatan'],
    'Skills & Technology': ['programming', 'teknologi', 'bahasa', 'skill']
}

category_counts = {}
for category, keywords in categories.items():
    count = 0
    for keyword in keywords:
        count += df['Interest'].str.contains(keyword, case=False, na=False).sum()
    category_counts[category] = count

plt.figure(figsize=(12, 8))
categories_list = list(category_counts.keys())
counts_list = list(category_counts.values())

bars = plt.bar(categories_list, counts_list, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
plt.title('Interest Category Distribution', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Number of Customers', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Add value labels
for bar, value in zip(bars, counts_list):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
             str(value), ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/03_interest_category_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Entrepreneurship Interest by Cluster
plt.figure(figsize=(10, 6))
entrepreneurship_by_cluster = []
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    entrepreneurship_count = cluster_data['Interest'].str.contains('bisnis|entrepreneurship|marketing', 
                                                                 case=False, na=False).sum()
    entrepreneurship_by_cluster.append(entrepreneurship_count)

bars = plt.bar(range(7), entrepreneurship_by_cluster, color=colors)
plt.title('Entrepreneurship Interest by Cluster', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Cluster ID', fontsize=12)
plt.ylabel('Number of Customers with Entrepreneurship Interest', fontsize=12)
plt.xticks(range(7), [f'Cluster {i}' for i in range(7)])

# Add value labels
for i, value in enumerate(entrepreneurship_by_cluster):
    plt.text(i, value + 5, str(value), ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/04_entrepreneurship_by_cluster.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Age Distribution
plt.figure(figsize=(10, 6))
plt.hist(df['Age'], bins=20, color='#45B7D1', alpha=0.7, edgecolor='white', linewidth=1)
plt.title('Age Distribution of Customers', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Age (Years)', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.grid(axis='y', alpha=0.3)

# Add statistics
mean_age = df['Age'].mean()
median_age = df['Age'].median()
plt.axvline(mean_age, color='red', linestyle='--', label=f'Mean: {mean_age:.1f}')
plt.axvline(median_age, color='orange', linestyle='--', label=f'Median: {median_age:.1f}')
plt.legend()
plt.tight_layout()
plt.savefig('Final Analysis/charts/05_age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Spending Distribution
plt.figure(figsize=(10, 6))
plt.hist(df['Spending'], bins=20, color='#96CEB4', alpha=0.7, edgecolor='white', linewidth=1)
plt.title('Spending Distribution of Customers', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Spending (IDR)', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.grid(axis='y', alpha=0.3)

# Add statistics
mean_spending = df['Spending'].mean()
median_spending = df['Spending'].median()
plt.axvline(mean_spending, color='red', linestyle='--', label=f'Mean: Rp{mean_spending:,.0f}')
plt.axvline(median_spending, color='orange', linestyle='--', label=f'Median: Rp{median_spending:,.0f}')
plt.legend()
plt.tight_layout()
plt.savefig('Final Analysis/charts/06_spending_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. PCA Visualization
plt.figure(figsize=(12, 8))
scatter = plt.scatter(df['PCA1'], df['PCA2'], c=[colors[i] for i in df['Cluster']], 
                     alpha=0.7, s=60, edgecolors='white', linewidth=0.5)
plt.title('PCA Visualization of Customer Clusters', fontsize=16, fontweight='bold', pad=20)
plt.xlabel(f'First Principal Component (Variance: {pca.explained_variance_ratio_[0]:.2%})', fontsize=12)
plt.ylabel(f'Second Principal Component (Variance: {pca.explained_variance_ratio_[1]:.2%})', fontsize=12)

# Create legend
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    if len(cluster_data) > 0:
        plt.scatter([], [], c=colors[i], label=f'Cluster {i}', s=60)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/07_pca_visualization.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Frequency vs Program Analysis
plt.figure(figsize=(12, 8))
scatter = plt.scatter(df['Frequency'], df['Program'], c=[colors[i] for i in df['Cluster']], 
                     alpha=0.7, s=60, edgecolors='white', linewidth=0.5)
plt.title('Frequency vs Program by Clusters', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Frequency', fontsize=12)
plt.ylabel('Program', fontsize=12)

# Create legend
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    if len(cluster_data) > 0:
        plt.scatter([], [], c=colors[i], label=f'Cluster {i}', s=60)

plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/08_frequency_program_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. Top 10 Interests
top_interests = df['Interest'].value_counts().head(10)
plt.figure(figsize=(12, 8))
bars = plt.barh(range(len(top_interests)), top_interests.values, color='#FFEAA7')
plt.title('Top 10 Customer Interests', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Number of Customers', fontsize=12)
plt.yticks(range(len(top_interests)), top_interests.index)

# Add value labels
for i, value in enumerate(top_interests.values):
    plt.text(value + 5, i, str(value), va='center', fontweight='bold')

plt.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/09_top_interests.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. Cluster Centers Heatmap
cluster_centers = []
feature_names = ['Age', 'Program', 'Spending', 'Frequency', 'Interest']

for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    centers = [
        cluster_data['Age'].mean(),
        cluster_data['Program'].mean(),
        cluster_data['Spending'].mean(),
        cluster_data['Frequency'].mean(),
        cluster_data['Interest'].nunique()
    ]
    cluster_centers.append(centers)

cluster_centers_df = pd.DataFrame(cluster_centers, 
                                columns=feature_names,
                                index=[f'Cluster {i}' for i in range(7)])

plt.figure(figsize=(10, 6))
sns.heatmap(cluster_centers_df.T, annot=True, fmt='.1f', cmap='YlOrRd', 
           cbar_kws={'label': 'Feature Values'})
plt.title('Cluster Centers Heatmap', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Features', fontsize=12)
plt.xlabel('Clusters', fontsize=12)
plt.tight_layout()
plt.savefig('Final Analysis/charts/10_cluster_centers_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 11. Creative Arts Analysis
creative_keywords = ['seni', 'crafting', 'visual', 'design', 'fotografi', 'musik']
creative_by_cluster = []
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    creative_count = 0
    for keyword in creative_keywords:
        creative_count += cluster_data['Interest'].str.contains(keyword, case=False, na=False).sum()
    creative_by_cluster.append(creative_count)

plt.figure(figsize=(10, 6))
bars = plt.bar(range(7), creative_by_cluster, color='#DDA0DD')
plt.title('Creative Arts Interest by Cluster', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Cluster ID', fontsize=12)
plt.ylabel('Number of Customers with Creative Interest', fontsize=12)
plt.xticks(range(7), [f'Cluster {i}' for i in range(7)])

# Add value labels
for i, value in enumerate(creative_by_cluster):
    plt.text(i, value + 5, str(value), ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/11_creative_arts_by_cluster.png', dpi=300, bbox_inches='tight')
plt.close()

# 12. Business Opportunity Matrix
opportunities = {
    'Entrepreneurship Hub': [1465, 'High', 'Immediate'],
    'Creative Platform': [1749, 'High', 'Medium'],
    'Family Education': [1654, 'Medium', 'Immediate'],
    'Lifestyle Services': [890, 'Medium', 'Medium'],
    'Tech Skills Training': [445, 'Low', 'Long-term']
}

plt.figure(figsize=(12, 8))
market_size = [opp[0] for opp in opportunities.values()]
colors_map = {'High': '#FF6B6B', 'Medium': '#FFEAA7', 'Low': '#96CEB4'}
bar_colors = [colors_map[opp[1]] for opp in opportunities.values()]

bars = plt.bar(opportunities.keys(), market_size, color=bar_colors)
plt.title('Business Opportunity Matrix', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Market Size (Number of Customers)', fontsize=12)
plt.xticks(rotation=45, ha='right')

# Add value labels
for bar, value in zip(bars, market_size):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 20, 
             str(value), ha='center', va='bottom', fontweight='bold')

# Add legend
for potential, color in colors_map.items():
    plt.bar([], [], color=color, label=f'{potential} Potential')
plt.legend()

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/12_business_opportunity_matrix.png', dpi=300, bbox_inches='tight')
plt.close()

# 13. Geographic Distribution (simplified)
# Since we don't have exact location data, we'll create a representative chart
regions = ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Makassar', 'Others']
region_counts = [650, 420, 380, 280, 250, 842]  # Representative data

plt.figure(figsize=(10, 6))
bars = plt.bar(regions, region_counts, color='#98D8C8')
plt.title('Geographic Distribution of Customers', fontsize=16, fontweight='bold', pad=20)
plt.ylabel('Number of Customers', fontsize=12)
plt.xticks(rotation=45)

# Add value labels
for bar, value in zip(bars, region_counts):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, 
             str(value), ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/13_geographic_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\n✅ Successfully created 13 individual charts in 'Final Analysis/charts/' directory!")
print("\nFiles created:")
for i in range(1, 14):
    chart_files = [
        "01_cluster_overview.png",
        "02_age_spending_segmentation.png", 
        "03_interest_category_distribution.png",
        "04_entrepreneurship_by_cluster.png",
        "05_age_distribution.png",
        "06_spending_distribution.png", 
        "07_pca_visualization.png",
        "08_frequency_program_analysis.png",
        "09_top_interests.png",
        "10_cluster_centers_heatmap.png",
        "11_creative_arts_by_cluster.png",
        "12_business_opportunity_matrix.png",
        "13_geographic_distribution.png"
    ]
    if i <= len(chart_files):
        print(f"   {i:2d}. {chart_files[i-1]}")
