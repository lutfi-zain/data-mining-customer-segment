import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import os
import warnings
warnings.filterwarnings('ignore')

print("Debugging and fixing creative arts chart...")

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

print("Data prepared successfully...")
print(f"Dataset shape: {df.shape}")
print(f"Unique clusters: {df['Cluster'].nunique()}")

# Analyze creative arts interests more thoroughly
creative_keywords = ['seni', 'crafting', 'visual', 'design', 'fotografi', 'musik', 'kreativitas', 'kreatif', 'drawing', 'art']

print("\nAnalyzing creative interests...")
print("Available Sub_Kategori_1 values:")
print(df['Sub_Kategori_1'].value_counts().head(10))

print("\nAvailable Sub_Kategori_2 values:")
print(df['Sub_Kategori_2'].value_counts().head(10))

# Check for creative interests
creative_by_cluster = []
creative_details = []

for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    creative_count = 0
    
    # Check in all sub-categories
    for keyword in creative_keywords:
        count1 = cluster_data['Sub_Kategori_1'].str.contains(keyword, case=False, na=False).sum()
        count2 = cluster_data['Sub_Kategori_2'].str.contains(keyword, case=False, na=False).sum()
        count3 = cluster_data['Sub_Kategori_3'].str.contains(keyword, case=False, na=False).sum()
        count4 = cluster_data['Sub_Kategori_4'].str.contains(keyword, case=False, na=False).sum()
        
        total_count = count1 + count2 + count3 + count4
        creative_count += total_count
        
        if total_count > 0:
            print(f"Cluster {i}, Keyword '{keyword}': {total_count} occurrences")
    
    creative_by_cluster.append(creative_count)
    creative_details.append({
        'cluster': i,
        'size': len(cluster_data),
        'creative_count': creative_count,
        'percentage': (creative_count / len(cluster_data) * 100) if len(cluster_data) > 0 else 0
    })

print(f"\nCreative counts by cluster: {creative_by_cluster}")

for detail in creative_details:
    print(f"Cluster {detail['cluster']}: {detail['creative_count']} creative interests out of {detail['size']} customers ({detail['percentage']:.1f}%)")

# Create the corrected chart
plt.figure(figsize=(12, 8))
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8']

bars = plt.bar(range(7), creative_by_cluster, color=colors)
plt.title('Creative Arts Interest by Cluster', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Cluster ID', fontsize=12)
plt.ylabel('Number of Creative Interest Mentions', fontsize=12)
plt.xticks(range(7), [f'Cluster {i}' for i in range(7)])

# Add value labels on bars
for i, value in enumerate(creative_by_cluster):
    if value > 0:  # Only show label if there's a value
        plt.text(i, value + max(creative_by_cluster) * 0.01, str(value), 
                ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', alpha=0.3)

# Add subtitle with total
total_creative = sum(creative_by_cluster)
plt.figtext(0.5, 0.93, f'Total Creative Interest Mentions: {total_creative}', 
           ha='center', fontsize=11, style='italic')

plt.tight_layout()
plt.savefig('Final Analysis/charts/11_creative_arts_by_cluster.png', dpi=300, bbox_inches='tight')
plt.show()

print(f"\n✅ Chart saved successfully!")
print(f"Total creative interest mentions: {total_creative}")

# Also create a simplified version focusing on specific creative categories
print("\nCreating alternative creative analysis...")

# Focus on specific creative categories
creative_categories = {
    'Kreativitas Anak': 'Kreativitas dan Belajar Anak',
    'Motorik Anak': 'Motorik Anak', 
    'Hobi Kreatif': 'Hobi'
}

creative_alt_by_cluster = []
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    creative_alt_count = 0
    
    for category in creative_categories.values():
        count = cluster_data['Sub_Kategori_1'].str.contains(category, case=False, na=False).sum()
        creative_alt_count += count
    
    creative_alt_by_cluster.append(creative_alt_count)

print(f"Alternative creative counts: {creative_alt_by_cluster}")

plt.figure(figsize=(12, 8))
bars = plt.bar(range(7), creative_alt_by_cluster, color='#DDA0DD')
plt.title('Creative Development Interest by Cluster\n(Child Creativity & Motor Skills Focus)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Cluster ID', fontsize=12)
plt.ylabel('Number of Customers with Creative Development Interest', fontsize=12)
plt.xticks(range(7), [f'Cluster {i}' for i in range(7)])

# Add value labels
for i, value in enumerate(creative_alt_by_cluster):
    if value > 0:
        plt.text(i, value + max(creative_alt_by_cluster) * 0.01, str(value), 
                ha='center', va='bottom', fontweight='bold')

plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('Final Analysis/charts/11_creative_arts_by_cluster_alt.png', dpi=300, bbox_inches='tight')
plt.show()

print("✅ Alternative chart also saved!")
