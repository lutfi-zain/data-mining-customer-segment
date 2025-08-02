import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

print("Creating optimized creative arts chart...")

# Read the data
df = pd.read_csv('01_data/data.csv')

# Rename columns for consistency
df.columns = ['Usia', 'Domisili', 'Nama_Program', 'Harga_Kelas', 'Kategori', 
              'Sub_Kategori_1', 'Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']

# Create feature columns
df['Age'] = df['Usia']
df['Program'] = df['Nama_Program'].astype('category').cat.codes
df['Spending'] = df['Harga_Kelas']
df['Frequency'] = 1
df['Interest'] = df['Sub_Kategori_1'].fillna('') + ' ' + df['Sub_Kategori_2'].fillna('')

# Prepare data for clustering
feature_columns = ['Age', 'Program', 'Spending', 'Frequency']
X = df[feature_columns].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Apply K-means clustering
kmeans = KMeans(n_clusters=7, random_state=42)
df['Cluster'] = kmeans.fit_predict(X_scaled)

# Focus on key creative categories - count unique customers, not mentions
creative_keywords = ['Kreativitas', 'Motorik', 'Seni', 'Visual']

creative_customers_by_cluster = []
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    
    # Create boolean mask for customers with any creative interest
    creative_mask = False
    for keyword in creative_keywords:
        keyword_mask = (
            cluster_data['Sub_Kategori_1'].str.contains(keyword, case=False, na=False) |
            cluster_data['Sub_Kategori_2'].str.contains(keyword, case=False, na=False) |
            cluster_data['Sub_Kategori_3'].str.contains(keyword, case=False, na=False) |
            cluster_data['Sub_Kategori_4'].str.contains(keyword, case=False, na=False)
        )
        creative_mask = creative_mask | keyword_mask
    
    creative_customers = creative_mask.sum()
    creative_customers_by_cluster.append(creative_customers)

print(f"Creative customers by cluster: {creative_customers_by_cluster}")

# Create a professional chart
plt.figure(figsize=(12, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

bars = plt.bar(range(7), creative_customers_by_cluster, color=colors)
plt.title('Customers with Creative Arts Interests by Cluster', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Cluster ID', fontsize=12)
plt.ylabel('Number of Customers', fontsize=12)
plt.xticks(range(7), [f'Cluster {i}' for i in range(7)])

# Add value labels on bars
max_value = max(creative_customers_by_cluster)
for i, value in enumerate(creative_customers_by_cluster):
    if value > 0:
        plt.text(i, value + max_value * 0.01, str(value), 
                ha='center', va='bottom', fontweight='bold', fontsize=11)

# Add percentage labels
cluster_sizes = df['Cluster'].value_counts().sort_index()
for i, (value, size) in enumerate(zip(creative_customers_by_cluster, cluster_sizes)):
    if value > 0:
        percentage = (value / size) * 100
        plt.text(i, value * 0.5, f'{percentage:.1f}%', 
                ha='center', va='center', fontweight='bold', 
                color='white', fontsize=10)

plt.grid(axis='y', alpha=0.3)

# Add subtitle with summary
total_creative_customers = sum(creative_customers_by_cluster)
total_customers = len(df)
overall_percentage = (total_creative_customers / total_customers) * 100
plt.figtext(0.5, 0.93, f'Total Creative Customers: {total_creative_customers} ({overall_percentage:.1f}% of customer base)', 
           ha='center', fontsize=11, style='italic')

plt.tight_layout()
plt.savefig('Final Analysis/charts/11_creative_arts_by_cluster.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"✅ Optimized chart saved!")
print(f"Total creative customers: {total_creative_customers} ({overall_percentage:.1f}%)")

# Create cluster size reference chart for comparison
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
bars1 = plt.bar(range(7), cluster_sizes, color=colors, alpha=0.7)
plt.title('Total Customers by Cluster', fontsize=14, fontweight='bold')
plt.xlabel('Cluster ID')
plt.ylabel('Number of Customers')
plt.xticks(range(7), [f'C{i}' for i in range(7)])

for i, value in enumerate(cluster_sizes):
    plt.text(i, value + max(cluster_sizes) * 0.01, str(value), 
            ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.subplot(1, 2, 2)
bars2 = plt.bar(range(7), creative_customers_by_cluster, color=colors)
plt.title('Creative Arts Customers by Cluster', fontsize=14, fontweight='bold')
plt.xlabel('Cluster ID')
plt.ylabel('Creative Customers')
plt.xticks(range(7), [f'C{i}' for i in range(7)])

for i, value in enumerate(creative_customers_by_cluster):
    if value > 0:
        plt.text(i, value + max(creative_customers_by_cluster) * 0.01, str(value), 
                ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig('Final Analysis/charts/11_creative_arts_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

print("✅ Comparison chart also created!")

# Print detailed breakdown
print("\nDetailed Creative Arts Analysis:")
print("Cluster | Total | Creative | Percentage")
print("--------|-------|----------|----------")
for i in range(7):
    total = cluster_sizes[i]
    creative = creative_customers_by_cluster[i]
    percentage = (creative / total) * 100 if total > 0 else 0
    print(f"   {i}    |  {total:3d}  |   {creative:3d}    |  {percentage:5.1f}%")
