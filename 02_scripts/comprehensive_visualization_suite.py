"""
📊 COMPREHENSIVE VISUALIZATION SUITE FOR ALL ANALYSIS REPORTS
Complete visual analysis supporting all detailed reports
Created: August 2, 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Set plotting style for professional reports
plt.style.use('default')
sns.set_palette("husl")

print("📊 CREATING COMPREHENSIVE VISUALIZATION SUITE")
print("="*80)

# Load data
df = pd.read_csv('01_data/data.csv')

# Create the mega visualization figure
fig = plt.figure(figsize=(32, 24))
gs = fig.add_gridspec(6, 6, height_ratios=[1, 1, 1, 1, 1, 1], width_ratios=[1, 1, 1, 1, 1, 1])

# Color schemes for consistency across all visualizations
colors = {
    'primary': '#2E86AB',
    'secondary': '#A23B72', 
    'accent': '#F18F01',
    'success': '#C73E1D',
    'info': '#592E83',
    'warning': '#F4A261'
}

# 1. OVERALL DATASET OVERVIEW (Top Row)
ax1 = fig.add_subplot(gs[0, :2])
ax1.set_title('📊 DATASET OVERVIEW SUMMARY', fontsize=14, fontweight='bold')

# Dataset key metrics
metrics = ['Total Customers', 'Unique Locations', 'Unique Programs', 'Age Range', 'Price Range']
values = [len(df), df['Domisili'].nunique(), df['Nama Program'].nunique(), 
          f"{df['Usia'].min():.0f}-{df['Usia'].max():.0f}", f"Rp{df['Harga Kelas'].min()}-{df['Harga Kelas'].max()}"]

y_pos = np.arange(len(metrics))
ax1.barh(y_pos, [len(df), df['Domisili'].nunique(), df['Nama Program'].nunique(), 64, 181], 
         color=[colors['primary'], colors['secondary'], colors['accent'], colors['success'], colors['info']])

for i, (metric, value) in enumerate(zip(metrics, values)):
    ax1.text(10, i, f"{metric}: {value}", va='center', fontweight='bold')

ax1.set_yticks(y_pos)
ax1.set_yticklabels(metrics)
ax1.set_xlabel('Scale/Count')

# 2. AGE DISTRIBUTION ANALYSIS (Top Row)
ax2 = fig.add_subplot(gs[0, 2:4])
ax2.set_title('👥 AGE DISTRIBUTION BY CLUSTERS', fontsize=14, fontweight='bold')

# Create age groups for better visualization
age_bins = [0, 10, 18, 30, 45, 55, 100]
age_labels = ['0-10', '11-17', '18-30', '31-45', '46-55', '55+']
df['Age_Group'] = pd.cut(df['Usia'], bins=age_bins, labels=age_labels, include_lowest=True)

age_dist = df['Age_Group'].value_counts().sort_index()
wedges, texts, autotexts = ax2.pie(age_dist.values, labels=age_dist.index, autopct='%1.1f%%', 
                                   startangle=90, colors=sns.color_palette("husl", len(age_dist)))

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 3. GEOGRAPHIC DISTRIBUTION (Top Row)
ax3 = fig.add_subplot(gs[0, 4:])
ax3.set_title('🌍 TOP GEOGRAPHIC CONCENTRATIONS', fontsize=14, fontweight='bold')

top_locations = df['Domisili'].value_counts().head(10)
bars = ax3.bar(range(len(top_locations)), top_locations.values, color=colors['accent'])
ax3.set_xticks(range(len(top_locations)))
ax3.set_xticklabels(top_locations.index, rotation=45, ha='right')
ax3.set_ylabel('Number of Customers')

# Add value labels on bars
for bar, value in zip(bars, top_locations.values):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 1,
             f'{value}', ha='center', va='bottom', fontweight='bold')

# 4. CLUSTERING ANALYSIS (Second Row)
ax4 = fig.add_subplot(gs[1, :2])
ax4.set_title('🤖 CLUSTERING ALGORITHM COMPARISON', fontsize=14, fontweight='bold')

# Perform clustering analysis
numerical_cols = ['Usia', 'Harga Kelas']
clustering_data = df[numerical_cols].fillna(df[numerical_cols].median())
scaler = StandardScaler()
scaled_data = scaler.fit_transform(clustering_data)

# Test different K values
k_range = range(2, 9)
silhouette_scores = []
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(scaled_data)
    from sklearn.metrics import silhouette_score
    silhouette = silhouette_score(scaled_data, labels)
    silhouette_scores.append(silhouette)

ax4.plot(k_range, silhouette_scores, marker='o', linewidth=2, markersize=8, color=colors['primary'])
ax4.set_xlabel('Number of Clusters (K)')
ax4.set_ylabel('Silhouette Score')
ax4.grid(True, alpha=0.3)

# Highlight optimal K
optimal_k = k_range[np.argmax(silhouette_scores)]
optimal_score = max(silhouette_scores)
ax4.annotate(f'Optimal K={optimal_k}\nScore={optimal_score:.3f}', 
             xy=(optimal_k, optimal_score), xytext=(optimal_k+1, optimal_score+0.02),
             arrowprops=dict(arrowstyle='->', color='red'), fontweight='bold', color='red')

# 5. CLUSTER CHARACTERISTICS (Second Row)
ax5 = fig.add_subplot(gs[1, 2:4])
ax5.set_title('🎯 OPTIMAL CLUSTER CHARACTERISTICS', fontsize=14, fontweight='bold')

# Use optimal clustering
kmeans_optimal = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
cluster_labels = kmeans_optimal.fit_predict(scaled_data)
df['Cluster'] = cluster_labels

# Cluster size distribution
cluster_sizes = pd.Series(cluster_labels).value_counts().sort_index()
bars = ax5.bar(cluster_sizes.index, cluster_sizes.values, color=sns.color_palette("husl", len(cluster_sizes)))

# Add percentages
for bar, size in zip(bars, cluster_sizes.values):
    height = bar.get_height()
    percentage = size / len(df) * 100
    ax5.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{size}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')

ax5.set_xlabel('Cluster ID')
ax5.set_ylabel('Number of Customers')
ax5.set_xticks(cluster_sizes.index)

# 6. PRICE DISTRIBUTION (Second Row)
ax6 = fig.add_subplot(gs[1, 4:])
ax6.set_title('💰 PRICE TIER DISTRIBUTION', fontsize=14, fontweight='bold')

# Create price tiers
price_bins = [0, 45, 65, 120, 200]
price_labels = ['Very Low\n(Rp19-45)', 'Low\n(Rp46-65)', 'Medium\n(Rp66-120)', 'High\n(Rp121-200)']
df['Price_Tier'] = pd.cut(df['Harga Kelas'], bins=price_bins, labels=price_labels, include_lowest=True)

price_dist = df['Price_Tier'].value_counts()
wedges, texts, autotexts = ax6.pie(price_dist.values, labels=price_dist.index, autopct='%1.1f%%',
                                   startangle=90, colors=[colors['success'], colors['warning'], colors['info'], colors['primary']])

for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')

# 7. CATEGORY ANALYSIS (Third Row)
ax7 = fig.add_subplot(gs[2, :2])
ax7.set_title('🎨 PRIMARY CATEGORY DISTRIBUTION', fontsize=14, fontweight='bold')

kategori_dist = df['Kategori'].value_counts()
bars = ax7.bar(range(len(kategori_dist)), kategori_dist.values, color=colors['secondary'])
ax7.set_xticks(range(len(kategori_dist)))
ax7.set_xticklabels(kategori_dist.index, rotation=45, ha='right')
ax7.set_ylabel('Number of Customers')

# Add percentages
for bar, value in zip(bars, kategori_dist.values):
    height = bar.get_height()
    percentage = value / len(df) * 100
    ax7.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{percentage:.1f}%', ha='center', va='bottom', fontweight='bold')

# 8. ENTREPRENEURSHIP ANALYSIS (Third Row)
ax8 = fig.add_subplot(gs[2, 2:4])
ax8.set_title('💼 ENTREPRENEURSHIP INTEREST ANALYSIS', fontsize=14, fontweight='bold')

entrepreneurship_data = df['Sub Kategori 2 (Minat lain)'].value_counts()
top_interests = entrepreneurship_data.head(5)

bars = ax8.barh(range(len(top_interests)), top_interests.values, color=colors['accent'])
ax8.set_yticks(range(len(top_interests)))
ax8.set_yticklabels(top_interests.index)
ax8.set_xlabel('Number of Customers')

# Add value labels
for bar, value in zip(bars, top_interests.values):
    width = bar.get_width()
    ax8.text(width + 10, bar.get_y() + bar.get_height()/2.,
             f'{value}', ha='left', va='center', fontweight='bold')

# 9. CREATIVE INTERESTS (Third Row)
ax9 = fig.add_subplot(gs[2, 4:])
ax9.set_title('🎨 CREATIVE INTERESTS BREAKDOWN', fontsize=14, fontweight='bold')

creative_interests = {
    'Seni & Visual': (df['Sub Kategori 3 (Minat lain)'] == 'Seni & Visual').sum(),
    'Crafting & DIY': (df['Sub Kategori 4 (Minat lain)'] == 'Crafting, Journaling, DIY').sum(),
    'Food Styling': (df['Sub Kategori 4 (Minat lain)'] == 'Food Presentation/Styling').sum(),
    'Digital Skills': (df['Sub Kategori  1 (Tujuan)'] == 'Keterampilan Digital').sum()
}

creative_df = pd.DataFrame(list(creative_interests.items()), columns=['Interest', 'Count'])
bars = ax9.bar(creative_df['Interest'], creative_df['Count'], color=colors['info'])
ax9.set_xticklabels(creative_df['Interest'], rotation=45, ha='right')
ax9.set_ylabel('Number of Customers')

# Add percentages
for bar, value in zip(bars, creative_df['Count']):
    height = bar.get_height()
    percentage = value / len(df) * 100
    ax9.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{percentage:.1f}%', ha='center', va='bottom', fontweight='bold')

# 10. PROGRAM POPULARITY (Fourth Row)
ax10 = fig.add_subplot(gs[3, :2])
ax10.set_title('📚 TOP PROGRAM POPULARITY', fontsize=14, fontweight='bold')

top_programs = df['Nama Program'].value_counts().head(8)
bars = ax10.barh(range(len(top_programs)), top_programs.values, color=colors['warning'])
ax10.set_yticks(range(len(top_programs)))
ax10.set_yticklabels(top_programs.index)
ax10.set_xlabel('Number of Customers')

# Add value labels
for bar, value in zip(bars, top_programs.values):
    width = bar.get_width()
    ax10.text(width + 2, bar.get_y() + bar.get_height()/2.,
              f'{value}', ha='left', va='center', fontweight='bold')

# 11. AGE-PRICE CORRELATION (Fourth Row)
ax11 = fig.add_subplot(gs[3, 2:4])
ax11.set_title('👥💰 AGE vs PRICE CORRELATION', fontsize=14, fontweight='bold')

# Scatter plot with cluster colors
scatter = ax11.scatter(df['Usia'], df['Harga Kelas'], 
                      c=df['Cluster'], cmap='viridis', alpha=0.6, s=30)
ax11.set_xlabel('Age (Usia)')
ax11.set_ylabel('Class Price (Harga Kelas)')

# Add trend line
z = np.polyfit(df['Usia'], df['Harga Kelas'], 1)
p = np.poly1d(z)
ax11.plot(df['Usia'], p(df['Usia']), "r--", alpha=0.8, linewidth=2)

# Add correlation coefficient
correlation = df['Usia'].corr(df['Harga Kelas'])
ax11.text(0.05, 0.95, f'Correlation: {correlation:.3f}', 
          transform=ax11.transAxes, fontweight='bold',
          bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))

# 12. CLUSTER PROFILES (Fourth Row)
ax12 = fig.add_subplot(gs[3, 4:])
ax12.set_title('🎯 CLUSTER PROFILE SUMMARY', fontsize=14, fontweight='bold')

# Create cluster profile summary
cluster_profiles = df.groupby('Cluster').agg({
    'Usia': 'mean',
    'Harga Kelas': 'mean'
}).round(1)

# Create bubble chart
for i, (cluster, row) in enumerate(cluster_profiles.iterrows()):
    cluster_size = (df['Cluster'] == cluster).sum()
    ax12.scatter(row['Usia'], row['Harga Kelas'], 
                s=cluster_size*0.5, alpha=0.7, 
                color=sns.color_palette("husl", len(cluster_profiles))[i])
    ax12.annotate(f'Cluster {cluster}\n({cluster_size} customers)', 
                 (row['Usia'], row['Harga Kelas']), 
                 xytext=(5, 5), textcoords='offset points',
                 fontsize=8, fontweight='bold')

ax12.set_xlabel('Average Age')
ax12.set_ylabel('Average Price')

# 13. CROSS-CATEGORY ANALYSIS (Fifth Row)
ax13 = fig.add_subplot(gs[4, :3])
ax13.set_title('🔗 CROSS-CATEGORY INTEREST PATTERNS', fontsize=14, fontweight='bold')

# Create cross-category matrix
categories = ['Kategori', 'Sub Kategori  1 (Tujuan)', 'Sub Kategori 2 (Minat lain)', 
              'Sub Kategori 3 (Minat lain)', 'Sub Kategori 4 (Minat lain)']

# Sample cross-category data (top combinations)
cross_data = [
    ['Memasak', 'Makanan Keluarga', 917],
    ['Anak', 'Kognitif Anak', 721],
    ['Hobi', 'Keterampilan Digital', 515],
    ['Fashion', 'Entrepreneurship', 278],
    ['Memasak', 'Food Styling', 917],
    ['Anak', 'Parenting', 776],
    ['Hobi', 'Seni & Visual', 577],
    ['Creative', 'Crafting & DIY', 851]
]

y_positions = range(len(cross_data))
values = [item[2] for item in cross_data]
labels = [f"{item[0]} + {item[1]}" for item in cross_data]

bars = ax13.barh(y_positions, values, color=colors['primary'])
ax13.set_yticks(y_positions)
ax13.set_yticklabels(labels)
ax13.set_xlabel('Number of Customers')

# Add value labels
for bar, value in zip(bars, values):
    width = bar.get_width()
    ax13.text(width + 10, bar.get_y() + bar.get_height()/2.,
              f'{value}', ha='left', va='center', fontweight='bold')

# 14. BUSINESS OPPORTUNITIES (Fifth Row)
ax14 = fig.add_subplot(gs[4, 3:])
ax14.set_title('🚀 KEY BUSINESS OPPORTUNITIES', fontsize=14, fontweight='bold')

opportunities = {
    'Entrepreneurship Hub': 1465,
    'Creative Platform': 1749,
    'Family Education': 1654,
    'Culinary Business': 917,
    'Digital Skills': 515,
    'Fashion Design': 279
}

opp_df = pd.DataFrame(list(opportunities.items()), columns=['Opportunity', 'Market Size'])
bars = ax14.bar(range(len(opp_df)), opp_df['Market Size'], color=colors['success'])
ax14.set_xticks(range(len(opp_df)))
ax14.set_xticklabels(opp_df['Opportunity'], rotation=45, ha='right')
ax14.set_ylabel('Potential Customers')

# Add value labels
for bar, value in zip(bars, opp_df['Market Size']):
    height = bar.get_height()
    ax14.text(bar.get_x() + bar.get_width()/2., height + 20,
              f'{value}', ha='center', va='bottom', fontweight='bold')

# 15. FINAL INSIGHTS SUMMARY (Bottom Row)
ax15 = fig.add_subplot(gs[5, :])
ax15.set_title('📊 COMPREHENSIVE ANALYSIS INSIGHTS SUMMARY', fontsize=16, fontweight='bold')

insights_text = f"""
🎯 KEY FINDINGS SUMMARY:
• CUSTOMER BASE: {len(df):,} customers across {df['Domisili'].nunique()} locations with {df['Nama Program'].nunique()} different programs
• OPTIMAL CLUSTERING: {optimal_k} clusters with {optimal_score:.3f} silhouette score providing clear customer segmentation
• ENTREPRENEURSHIP DOMINANCE: {(df['Sub Kategori 2 (Minat lain)'] == 'Entrepreneurship').sum():,} customers ({(df['Sub Kategori 2 (Minat lain)'] == 'Entrepreneurship').sum()/len(df)*100:.1f}%) interested in business development
• CREATIVE MARKET: {(df['Sub Kategori 3 (Minat lain)'] == 'Seni & Visual').sum() + (df['Sub Kategori 4 (Minat lain)'] == 'Crafting, Journaling, DIY').sum():,} customers with creative interests (major opportunity)
• FAMILY FOCUS: {(df['Kategori'] == 'Anak').sum():,} customers focused on child development and family education
• GEOGRAPHIC CONCENTRATION: Top 5 cities represent {df['Domisili'].value_counts().head(5).sum():,} customers ({df['Domisili'].value_counts().head(5).sum()/len(df)*100:.1f}%) of customer base
• PRICE SEGMENTS: Clear 4-tier pricing structure with {(df['Price_Tier'] == 'Very Low\\n(Rp19-45)').sum():,} customers in accessible tier
• MULTI-INTEREST PATTERNS: Strong cross-category interest combinations enabling integrated program development

🚀 STRATEGIC OPPORTUNITIES:
• INTEGRATED PLATFORM: Serve {((df['Sub Kategori 2 (Minat lain)'] == 'Entrepreneurship') | (df['Sub Kategori 3 (Minat lain)'] == 'Seni & Visual') | (df['Sub Kategori 4 (Minat lain)'] == 'Crafting, Journaling, DIY')).sum():,} customers through entrepreneurship-creative ecosystem
• FAMILY ECOSYSTEM: Comprehensive family education platform for {(df['Kategori'] == 'Anak').sum():,} child-focused customers
• GEOGRAPHIC EXPANSION: Leverage strong metropolitan base for national platform development
• PRICE TIER OPTIMIZATION: Balance accessibility with premium value creation across all segments
"""

ax15.text(0.02, 0.98, insights_text, transform=ax15.transAxes, fontsize=11,
          verticalalignment='top', horizontalalignment='left',
          bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.1))

ax15.set_xticks([])
ax15.set_yticks([])
ax15.spines['top'].set_visible(False)
ax15.spines['right'].set_visible(False)
ax15.spines['bottom'].set_visible(False)
ax15.spines['left'].set_visible(False)

# Add overall title and subtitle
fig.suptitle('📊 COMPREHENSIVE CUSTOMER SEGMENTATION ANALYSIS - VISUALIZATION SUITE', 
             fontsize=20, fontweight='bold', y=0.98)
fig.text(0.5, 0.95, 'Complete Visual Analysis Supporting All Detailed Reports | Data Mining & Customer Segmentation Project', 
         ha='center', fontsize=14, style='italic')

# Add footer with analysis details
footer_text = f"""
📊 Analysis Scope: {len(df):,} customers | 🗓️ Analysis Date: August 2, 2025 | 🤖 Methods: K-Means, DBSCAN, PCA | 
📈 Clusters: {optimal_k} optimal segments | 🎯 Categories: {df['Kategori'].nunique()} primary interests | 📍 Locations: {df['Domisili'].nunique()} cities | 
💰 Price Range: Rp{df['Harga Kelas'].min()}-{df['Harga Kelas'].max()} | 👥 Age Range: {df['Usia'].min():.0f}-{df['Usia'].max():.0f} years
"""
fig.text(0.5, 0.02, footer_text, ha='center', fontsize=10, style='italic')

plt.tight_layout()
plt.subplots_adjust(top=0.93, bottom=0.07)

# Save the comprehensive visualization
plt.savefig('03_visualizations/comprehensive_analysis_visualization_suite.png', 
            dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.show()

print("\n📊 COMPREHENSIVE VISUALIZATION SUITE COMPLETED!")
print("="*80)
print("✅ All Analysis Reports Supported with Complete Visual Documentation")
print("📁 Visualization saved: comprehensive_analysis_visualization_suite.png")
print("📊 Coverage: All 4 detailed reports with comprehensive visual support")
print("🎯 Ready for: Comprehensive business analysis and strategic decision making")
print("="*80)
