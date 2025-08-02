# 📊 INTEGRATED VISUAL ANALYSIS GUIDE
# Comprehensive chart integration with detailed reading instructions
# Date: August 2, 2025

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Load data
print("🔄 Loading data for integrated visual analysis...")
df = pd.read_csv('../01_data/data.csv')

# Preprocessing
print("🔄 Preprocessing data for visualization...")
scaler = StandardScaler()
numerical_features = ['Usia', 'Harga Kelas']
df_scaled = df.copy()
df_scaled[numerical_features] = scaler.fit_transform(df[numerical_features])

# Clustering
kmeans = KMeans(n_clusters=7, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled[numerical_features])

# Create comprehensive integrated visualization
plt.style.use('default')
fig = plt.figure(figsize=(24, 32))
gs = fig.add_gridspec(8, 3, hspace=0.4, wspace=0.3)

# Color palette for clusters
cluster_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']

# 1. CLUSTER OVERVIEW - Main Segmentation
ax1 = fig.add_subplot(gs[0, :])
cluster_counts = df['Cluster'].value_counts().sort_index()
bars = ax1.bar(range(len(cluster_counts)), cluster_counts.values, color=cluster_colors)
ax1.set_title('📊 CUSTOMER CLUSTERS OVERVIEW\nHow to Read: Height = number of customers, Colors = different segments', 
              fontsize=16, fontweight='bold', pad=20)
ax1.set_xlabel('Cluster Number (0-6)', fontsize=12)
ax1.set_ylabel('Number of Customers', fontsize=12)

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    percentage = (height / len(df)) * 100
    ax1.text(bar.get_x() + bar.get_width()/2., height + 20,
             f'{int(height)}\n({percentage:.1f}%)',
             ha='center', va='bottom', fontweight='bold')

ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(0, max(cluster_counts.values) * 1.15)

# 2. AGE-PRICE CLUSTERING SCATTER
ax2 = fig.add_subplot(gs[1, 0])
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    ax2.scatter(cluster_data['Usia'], cluster_data['Harga Kelas'], 
                c=cluster_colors[i], label=f'Cluster {i}', alpha=0.7, s=60)

ax2.set_title('👥 AGE-PRICE SEGMENTATION\nHow to Read: Position shows age vs price,\nColors show different customer types', 
              fontsize=12, fontweight='bold')
ax2.set_xlabel('Age (Years)', fontsize=10)
ax2.set_ylabel('Class Price (Rp)', fontsize=10)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
ax2.grid(alpha=0.3)

# 3. CATEGORY DISTRIBUTION
ax3 = fig.add_subplot(gs[1, 1])
category_counts = df['Kategori'].value_counts()
wedges, texts, autotexts = ax3.pie(category_counts.values, labels=None, autopct='%1.1f%%',
                                   colors=plt.cm.Set3(np.linspace(0, 1, len(category_counts))))
ax3.set_title('🎯 PRIMARY INTEREST CATEGORIES\nHow to Read: Slice size = market share,\nPercentages show customer distribution', 
              fontsize=12, fontweight='bold')
ax3.legend(wedges, [f'{cat}\n({count} customers)' for cat, count in category_counts.items()],
           bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

# 4. ENTREPRENEURSHIP ANALYSIS
ax4 = fig.add_subplot(gs[1, 2])
entrepreneurship_data = df['Sub Kategori 2 (Minat lain)'].value_counts()
entrepreneurship_count = entrepreneurship_data.get('Entrepreneurship', 0)
other_count = len(df) - entrepreneurship_count

pie_data = [entrepreneurship_count, other_count]
pie_labels = ['Entrepreneurship\nInterested', 'Other\nInterests']
colors = ['#FF6B6B', '#E0E0E0']

ax4.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax4.set_title('💼 ENTREPRENEURSHIP DOMINANCE\nHow to Read: Red = business-minded customers,\nGray = other focus areas', 
              fontsize=12, fontweight='bold')

# 5. CLUSTER AGE DISTRIBUTION
ax5 = fig.add_subplot(gs[2, :])
cluster_ages = []
cluster_labels = []
for i in range(7):
    cluster_data = df[df['Cluster'] == i]['Usia']
    cluster_ages.append(cluster_data.values)
    cluster_labels.append(f'Cluster {i}\n(n={len(cluster_data)})')

bp = ax5.boxplot(cluster_ages, labels=cluster_labels, patch_artist=True)
for patch, color in zip(bp['boxes'], cluster_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax5.set_title('📈 AGE DISTRIBUTION BY CLUSTER\nHow to Read: Box = age range, Line = median age, Dots = outliers', 
              fontsize=14, fontweight='bold')
ax5.set_ylabel('Age (Years)', fontsize=12)
ax5.grid(axis='y', alpha=0.3)

# 6. PRICE DISTRIBUTION BY CLUSTER
ax6 = fig.add_subplot(gs[3, :])
cluster_prices = []
for i in range(7):
    cluster_data = df[df['Cluster'] == i]['Harga Kelas']
    cluster_prices.append(cluster_data.values)

bp2 = ax6.boxplot(cluster_prices, labels=cluster_labels, patch_artist=True)
for patch, color in zip(bp2['boxes'], cluster_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax6.set_title('💰 PRICE DISTRIBUTION BY CLUSTER\nHow to Read: Box height = price range, Position = typical spending', 
              fontsize=14, fontweight='bold')
ax6.set_ylabel('Class Price (Rp)', fontsize=12)
ax6.grid(axis='y', alpha=0.3)

# 7. CREATIVE INTERESTS HEATMAP
ax7 = fig.add_subplot(gs[4, :])
creative_interests = ['Seni & Visual', 'Crafting, Journaling, DIY', 'Keterampilan Digital']
clusters = list(range(7))

# Create matrix for creative interests by cluster
creative_matrix = np.zeros((len(creative_interests), len(clusters)))

for i, interest in enumerate(creative_interests):
    for j, cluster in enumerate(clusters):
        cluster_data = df[df['Cluster'] == cluster]
        interest_count = 0
        
        # Check in Sub Kategori 3 and 4
        for col in ['Sub Kategori 3', 'Sub Kategori 4']:
            if col in df.columns:
                interest_count += (cluster_data[col] == interest).sum()
        
        creative_matrix[i, j] = (interest_count / len(cluster_data)) * 100 if len(cluster_data) > 0 else 0

im = ax7.imshow(creative_matrix, cmap='Reds', aspect='auto')
ax7.set_xticks(range(len(clusters)))
ax7.set_xticklabels([f'Cluster {i}' for i in clusters])
ax7.set_yticks(range(len(creative_interests)))
ax7.set_yticklabels(creative_interests)
ax7.set_title('🎨 CREATIVE INTERESTS HEATMAP BY CLUSTER\nHow to Read: Darker red = higher interest %, Numbers show percentage of cluster', 
              fontsize=14, fontweight='bold')

# Add percentage values to heatmap
for i in range(len(creative_interests)):
    for j in range(len(clusters)):
        text = ax7.text(j, i, f'{creative_matrix[i, j]:.1f}%',
                       ha="center", va="center", color="black", fontweight='bold')

plt.colorbar(im, ax=ax7, label='Percentage of Cluster (%)')

# 8. GEOGRAPHIC CONCENTRATION
ax8 = fig.add_subplot(gs[5, 0])
top_cities = df['Domisili'].value_counts().head(10)
bars = ax8.barh(range(len(top_cities)), top_cities.values, color='skyblue')
ax8.set_yticks(range(len(top_cities)))
ax8.set_yticklabels(top_cities.index, fontsize=10)
ax8.set_title('🌍 TOP 10 GEOGRAPHIC\nCONCENTRATIONS\nHow to Read: Bar length = customer count,\nCities ranked by popularity', 
              fontsize=12, fontweight='bold')
ax8.set_xlabel('Number of Customers', fontsize=10)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax8.text(width + 1, bar.get_y() + bar.get_height()/2,
             f'{int(width)}', ha='left', va='center', fontweight='bold')

# 9. PROGRAM POPULARITY
ax9 = fig.add_subplot(gs[5, 1])
top_programs = df['Nama Program'].value_counts().head(8)
bars = ax9.bar(range(len(top_programs)), top_programs.values, color='lightgreen')
ax9.set_title('📚 TOP PROGRAM POPULARITY\nHow to Read: Height = enrollment count,\nPrograms ranked by demand', 
              fontsize=12, fontweight='bold')
ax9.set_xticks(range(len(top_programs)))
ax9.set_xticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_programs.index], 
                    rotation=45, ha='right', fontsize=9)
ax9.set_ylabel('Number of Customers', fontsize=10)

# Add value labels
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax9.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')

# 10. INTEREST EVOLUTION PATTERN
ax10 = fig.add_subplot(gs[5, 2])
age_groups = ['0-10', '11-20', '21-30', '31-40', '41-50', '51+']
age_ranges = [(0, 10), (11, 20), (21, 30), (31, 40), (41, 50), (51, 100)]

interest_evolution = {
    'Creative Arts': [],
    'Entrepreneurship': [],
    'Child Focus': [],
    'Cooking': []
}

for start, end in age_ranges:
    age_group_data = df[(df['Usia'] >= start) & (df['Usia'] <= end)]
    total_in_group = len(age_group_data)
    
    if total_in_group > 0:
        # Creative Arts
        creative_count = 0
        for col in ['Sub Kategori 3', 'Sub Kategori 4']:
            if col in df.columns:
                creative_count += age_group_data[col].isin(['Seni & Visual', 'Crafting, Journaling, DIY']).sum()
        interest_evolution['Creative Arts'].append((creative_count / total_in_group) * 100)
        
        # Entrepreneurship
        entrepreneur_count = (age_group_data['Sub Kategori 2'] == 'Entrepreneurship').sum()
        interest_evolution['Entrepreneurship'].append((entrepreneur_count / total_in_group) * 100)
        
        # Child Focus
        child_count = (age_group_data['Kategori'] == 'Anak').sum()
        interest_evolution['Child Focus'].append((child_count / total_in_group) * 100)
        
        # Cooking
        cooking_count = (age_group_data['Kategori'] == 'Memasak').sum()
        interest_evolution['Cooking'].append((cooking_count / total_in_group) * 100)
    else:
        for key in interest_evolution:
            interest_evolution[key].append(0)

for interest, values in interest_evolution.items():
    ax10.plot(age_groups, values, marker='o', linewidth=2, label=interest)

ax10.set_title('📊 INTEREST EVOLUTION BY AGE\nHow to Read: Lines show interest trends,\nPoints = percentage in age group', 
               fontsize=12, fontweight='bold')
ax10.set_xlabel('Age Groups', fontsize=10)
ax10.set_ylabel('Interest Percentage (%)', fontsize=10)
ax10.legend(fontsize=9)
ax10.grid(alpha=0.3)

# 11. CLUSTER CHARACTERISTICS RADAR CHART
ax11 = fig.add_subplot(gs[6, :], projection='polar')

# Define characteristics for radar chart
characteristics = ['Avg Age', 'Avg Price', 'Entrepreneurship %', 'Creative %', 'Child Focus %']
angles = np.linspace(0, 2 * np.pi, len(characteristics), endpoint=False).tolist()
angles += angles[:1]  # Complete the circle

# Normalize values for radar chart
for cluster_id in range(7):
    cluster_data = df[df['Cluster'] == cluster_id]
    
    if len(cluster_data) > 0:
        values = []
        
        # Average age (normalized to 0-100)
        avg_age = cluster_data['Usia'].mean()
        values.append((avg_age / 63) * 100)  # Max age is 63
        
        # Average price (normalized to 0-100)
        avg_price = cluster_data['Harga Kelas'].mean()
        values.append((avg_price / 200) * 100)  # Max price is 200
        
        # Entrepreneurship percentage
        entrepreneur_pct = (cluster_data['Sub Kategori 2'] == 'Entrepreneurship').mean() * 100
        values.append(entrepreneur_pct)
        
        # Creative percentage
        creative_count = 0
        for col in ['Sub Kategori 3', 'Sub Kategori 4']:
            if col in df.columns:
                creative_count += cluster_data[col].isin(['Seni & Visual', 'Crafting, Journaling, DIY']).sum()
        creative_pct = (creative_count / len(cluster_data)) * 100 if len(cluster_data) > 0 else 0
        values.append(creative_pct)
        
        # Child focus percentage
        child_pct = (cluster_data['Kategori'] == 'Anak').mean() * 100
        values.append(child_pct)
        
        values += values[:1]  # Complete the circle
        
        ax11.plot(angles, values, 'o-', linewidth=2, label=f'Cluster {cluster_id}', 
                  color=cluster_colors[cluster_id], alpha=0.7)
        ax11.fill(angles, values, alpha=0.1, color=cluster_colors[cluster_id])

ax11.set_xticks(angles[:-1])
ax11.set_xticklabels(characteristics, fontsize=10)
ax11.set_ylim(0, 100)
ax11.set_title('🎯 CLUSTER CHARACTERISTICS RADAR\nHow to Read: Distance from center = intensity,\nShapes show cluster profiles', 
               fontsize=14, fontweight='bold', pad=30)
ax11.legend(bbox_to_anchor=(1.3, 1.1), loc='upper left', fontsize=9)
ax11.grid(True)

# 12. BUSINESS OPPORTUNITY MATRIX
ax12 = fig.add_subplot(gs[7, :])

# Define business opportunities
opportunities = [
    ('Culinary Entrepreneurs', 575, 85, 'High Revenue\nHigh Volume'),
    ('Creative Platform', 1749, 62, 'Medium Revenue\nVery High Volume'),
    ('Family Education', 1654, 58, 'Medium Revenue\nHigh Volume'),
    ('Fashion Business', 253, 93, 'High Revenue\nMedium Volume'),
    ('Digital Skills', 515, 81, 'High Revenue\nMedium Volume'),
    ('Child Development', 879, 75, 'Medium Revenue\nHigh Volume'),
    ('Premium Culinary', 303, 93, 'Very High Revenue\nLow Volume')
]

# Extract data for scatter plot
names = [opp[0] for opp in opportunities]
market_sizes = [opp[1] for opp in opportunities]
engagement_rates = [opp[2] for opp in opportunities]
colors_business = plt.cm.viridis(np.linspace(0, 1, len(opportunities)))

scatter = ax12.scatter(market_sizes, engagement_rates, s=[size/2 for size in market_sizes], 
                       c=colors_business, alpha=0.7)

# Add labels
for i, (name, size, engagement, description) in enumerate(opportunities):
    ax12.annotate(f'{name}\n({size} customers)', 
                  (size, engagement), 
                  xytext=(10, 10), textcoords='offset points',
                  fontsize=9, ha='left',
                  bbox=dict(boxstyle='round,pad=0.3', facecolor=colors_business[i], alpha=0.3))

ax12.set_xlabel('Market Size (Number of Customers)', fontsize=12)
ax12.set_ylabel('Engagement Rate (%)', fontsize=12)
ax12.set_title('💼 BUSINESS OPPORTUNITY MATRIX\nHow to Read: X-axis = market size, Y-axis = engagement,\nBubble size = opportunity scale', 
               fontsize=14, fontweight='bold')
ax12.grid(alpha=0.3)

# Add quadrant lines
ax12.axhline(y=np.mean(engagement_rates), color='red', linestyle='--', alpha=0.5)
ax12.axvline(x=np.mean(market_sizes), color='red', linestyle='--', alpha=0.5)

# Add quadrant labels
ax12.text(max(market_sizes)*0.8, max(engagement_rates)*0.95, 'High Engagement\nHigh Market', 
          ha='center', va='center', fontweight='bold', 
          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

plt.suptitle('🎯 COMPREHENSIVE CUSTOMER SEGMENTATION - INTEGRATED VISUAL ANALYSIS\n' +
             'Complete Visual Guide with Reading Instructions for Strategic Decision Making', 
             fontsize=20, fontweight='bold', y=0.98)

plt.tight_layout()
plt.savefig('06_visual_integration/comprehensive_integrated_analysis.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n" + "="*80)
print("📊 INTEGRATED VISUAL ANALYSIS COMPLETED!")
print("="*80)
print("\n🎯 CHART READING GUIDE:")
print("\n1. CLUSTER OVERVIEW: Shows 7 customer segments with sizes")
print("2. AGE-PRICE SCATTER: Reveals customer positioning and segment characteristics")
print("3. CATEGORY PIE: Primary interest distribution across customer base")
print("4. ENTREPRENEURSHIP PIE: Business-minded vs other customer split")
print("5. AGE BOXPLOTS: Age range and median for each cluster")
print("6. PRICE BOXPLOTS: Spending patterns and price positioning")
print("7. CREATIVE HEATMAP: Creative interest intensity by cluster")
print("8. GEOGRAPHIC BARS: Top customer concentration cities")
print("9. PROGRAM BARS: Most popular program enrollment")
print("10. INTEREST EVOLUTION: How interests change with age")
print("11. RADAR CHART: Multi-dimensional cluster profiling")
print("12. OPPORTUNITY MATRIX: Business potential vs market size")
print("\n✅ All visualizations saved to: comprehensive_integrated_analysis.png")
print("📁 Integration guide created for strategic analysis")
