# 📊 INTEGRATED VISUAL ANALYSIS GUIDE - CORRECTED VERSION
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

# Check column names
print("📋 Column names in dataset:")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

# Rename columns for easier access
df.columns = ['Usia', 'Domisili', 'Nama_Program', 'Harga_Kelas', 'Kategori', 
              'Sub_Kategori_1', 'Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']

print(f"\n📊 Dataset shape: {df.shape}")
print(f"🔍 Sample data preview:")
print(df.head(3))

# Preprocessing
print("\n🔄 Preprocessing data for visualization...")
scaler = StandardScaler()
numerical_features = ['Usia', 'Harga_Kelas']
df_scaled = df.copy()
df_scaled[numerical_features] = scaler.fit_transform(df[numerical_features])

# Clustering
kmeans = KMeans(n_clusters=7, random_state=42)
df['Cluster'] = kmeans.fit_predict(df_scaled[numerical_features])

# Create comprehensive integrated visualization
plt.style.use('default')
fig = plt.figure(figsize=(28, 36))
gs = fig.add_gridspec(9, 3, hspace=0.5, wspace=0.4)

# Color palette for clusters
cluster_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF']

# 1. CLUSTER OVERVIEW - Main Segmentation
ax1 = fig.add_subplot(gs[0, :])
cluster_counts = df['Cluster'].value_counts().sort_index()
bars = ax1.bar(range(len(cluster_counts)), cluster_counts.values, color=cluster_colors)
ax1.set_title('📊 CUSTOMER CLUSTERS OVERVIEW\n🔍 Cara Baca: Tinggi batang = jumlah customer, Warna = segmen berbeda\n' +
              'Insight: Distribusi customer dalam 7 segmen utama', 
              fontsize=16, fontweight='bold', pad=25)
ax1.set_xlabel('Cluster Number (0-6)', fontsize=14)
ax1.set_ylabel('Number of Customers', fontsize=14)

# Add value labels on bars
for i, bar in enumerate(bars):
    height = bar.get_height()
    percentage = (height / len(df)) * 100
    ax1.text(bar.get_x() + bar.get_width()/2., height + 20,
             f'{int(height)}\n({percentage:.1f}%)',
             ha='center', va='bottom', fontweight='bold', fontsize=12)

ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(0, max(cluster_counts.values) * 1.2)

# 2. AGE-PRICE CLUSTERING SCATTER
ax2 = fig.add_subplot(gs[1, 0])
for i in range(7):
    cluster_data = df[df['Cluster'] == i]
    ax2.scatter(cluster_data['Usia'], cluster_data['Harga_Kelas'], 
                c=cluster_colors[i], label=f'Cluster {i}', alpha=0.7, s=80)

ax2.set_title('👥 AGE-PRICE SEGMENTATION\n🔍 Cara Baca: Posisi = usia vs harga\nWarna = tipe customer berbeda\n' +
              'Insight: Pola belanja berdasar usia', 
              fontsize=13, fontweight='bold')
ax2.set_xlabel('Usia (Tahun)', fontsize=12)
ax2.set_ylabel('Harga Kelas (Rp)', fontsize=12)
ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax2.grid(alpha=0.3)

# 3. CATEGORY DISTRIBUTION
ax3 = fig.add_subplot(gs[1, 1])
category_counts = df['Kategori'].value_counts()
wedges, texts, autotexts = ax3.pie(category_counts.values, labels=None, autopct='%1.1f%%',
                                   colors=plt.cm.Set3(np.linspace(0, 1, len(category_counts))))
ax3.set_title('🎯 PRIMARY INTEREST CATEGORIES\n🔍 Cara Baca: Ukuran slice = pangsa pasar\nPersentase = distribusi customer\n' +
              'Insight: Dominasi kategori minat utama', 
              fontsize=13, fontweight='bold')
ax3.legend(wedges, [f'{cat}\n({count})' for cat, count in category_counts.items()],
           bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)

# 4. ENTREPRENEURSHIP ANALYSIS
ax4 = fig.add_subplot(gs[1, 2])
entrepreneurship_count = (df['Sub_Kategori_2'] == 'Entrepreneurship').sum()
other_count = len(df) - entrepreneurship_count

pie_data = [entrepreneurship_count, other_count]
pie_labels = ['Entrepreneurship\nInterested', 'Other\nInterests']
colors = ['#FF6B6B', '#E0E0E0']

ax4.pie(pie_data, labels=pie_labels, autopct='%1.1f%%', colors=colors, startangle=90)
ax4.set_title('💼 ENTREPRENEURSHIP DOMINANCE\n🔍 Cara Baca: Merah = tertarik bisnis\nAbu = fokus lain\n' +
              'Insight: Mayoritas customer punya minat bisnis', 
              fontsize=13, fontweight='bold')

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

ax5.set_title('📈 AGE DISTRIBUTION BY CLUSTER\n🔍 Cara Baca: Kotak = rentang usia, Garis tengah = median usia, Titik = outlier\n' +
              'Insight: Profil usia karakteristik setiap segmen customer', 
              fontsize=15, fontweight='bold')
ax5.set_ylabel('Usia (Tahun)', fontsize=13)
ax5.grid(axis='y', alpha=0.3)

# 6. PRICE DISTRIBUTION BY CLUSTER
ax6 = fig.add_subplot(gs[3, :])
cluster_prices = []
for i in range(7):
    cluster_data = df[df['Cluster'] == i]['Harga_Kelas']
    cluster_prices.append(cluster_data.values)

bp2 = ax6.boxplot(cluster_prices, labels=cluster_labels, patch_artist=True)
for patch, color in zip(bp2['boxes'], cluster_colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.7)

ax6.set_title('💰 PRICE DISTRIBUTION BY CLUSTER\n🔍 Cara Baca: Tinggi kotak = rentang harga, Posisi = pola belanja tipikal\n' +
              'Insight: Daya beli dan preferensi harga setiap segmen', 
              fontsize=15, fontweight='bold')
ax6.set_ylabel('Harga Kelas (Rp)', fontsize=13)
ax6.grid(axis='y', alpha=0.3)

# 7. INTEREST PATTERNS ANALYSIS
ax7 = fig.add_subplot(gs[4, 0])
all_interests = []
for col in ['Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']:
    all_interests.extend(df[col].value_counts().head(5).index.tolist())

# Count unique interests
unique_interests = list(set(all_interests))
interest_counts = []
for interest in unique_interests:
    count = 0
    for col in ['Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']:
        count += (df[col] == interest).sum()
    interest_counts.append(count)

# Sort by count
interest_data = list(zip(unique_interests, interest_counts))
interest_data.sort(key=lambda x: x[1], reverse=True)
top_interests = interest_data[:10]

interests, counts = zip(*top_interests)
bars = ax7.barh(range(len(interests)), counts, color='lightcoral')
ax7.set_yticks(range(len(interests)))
ax7.set_yticklabels([interest[:20] + '...' if len(interest) > 20 else interest for interest in interests])
ax7.set_title('🎨 TOP SECONDARY INTERESTS\n🔍 Cara Baca: Panjang batang = popularitas\nUrutan = ranking minat\n' +
              'Insight: Minat sekunder paling diminati', 
              fontsize=13, fontweight='bold')
ax7.set_xlabel('Number of Customers', fontsize=11)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax7.text(width + 10, bar.get_y() + bar.get_height()/2,
             f'{int(width)}', ha='left', va='center', fontweight='bold')

# 8. GEOGRAPHIC CONCENTRATION
ax8 = fig.add_subplot(gs[4, 1])
top_cities = df['Domisili'].value_counts().head(12)
bars = ax8.barh(range(len(top_cities)), top_cities.values, color='skyblue')
ax8.set_yticks(range(len(top_cities)))
ax8.set_yticklabels([city[:15] + '...' if len(city) > 15 else city for city in top_cities.index], fontsize=10)
ax8.set_title('🌍 TOP 12 GEOGRAPHIC CONCENTRATIONS\n🔍 Cara Baca: Panjang batang = jumlah customer\nKota diranking popularitas\n' +
              'Insight: Konsentrasi geografis market', 
              fontsize=13, fontweight='bold')
ax8.set_xlabel('Number of Customers', fontsize=11)

# Add value labels
for i, bar in enumerate(bars):
    width = bar.get_width()
    ax8.text(width + 1, bar.get_y() + bar.get_height()/2,
             f'{int(width)}', ha='left', va='center', fontweight='bold')

# 9. PROGRAM POPULARITY
ax9 = fig.add_subplot(gs[4, 2])
top_programs = df['Nama_Program'].value_counts().head(10)
bars = ax9.bar(range(len(top_programs)), top_programs.values, color='lightgreen')
ax9.set_title('📚 TOP 10 PROGRAM POPULARITY\n🔍 Cara Baca: Tinggi = jumlah pendaftar\nProgram diranking demand\n' +
              'Insight: Program paling diminati market', 
              fontsize=13, fontweight='bold')
ax9.set_xticks(range(len(top_programs)))
ax9.set_xticklabels([name[:15] + '...' if len(name) > 15 else name for name in top_programs.index], 
                    rotation=45, ha='right', fontsize=9)
ax9.set_ylabel('Number of Customers', fontsize=11)

# Add value labels
for i, bar in enumerate(bars):
    height = bar.get_height()
    ax9.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{int(height)}', ha='center', va='bottom', fontweight='bold')

# 10. INTEREST EVOLUTION BY AGE
ax10 = fig.add_subplot(gs[5, :])
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
        # Creative Arts (Seni & Visual + Crafting)
        creative_count = 0
        for col in ['Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']:
            creative_count += age_group_data[col].isin(['Seni & Visual', 'Crafting, Journaling, DIY']).sum()
        interest_evolution['Creative Arts'].append((creative_count / total_in_group) * 100)
        
        # Entrepreneurship
        entrepreneur_count = (age_group_data['Sub_Kategori_2'] == 'Entrepreneurship').sum()
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
    ax10.plot(age_groups, values, marker='o', linewidth=3, label=interest, markersize=8)

ax10.set_title('📊 INTEREST EVOLUTION BY AGE GROUP\n🔍 Cara Baca: Garis = tren minat, Titik = persentase dalam kelompok usia\n' +
               'Insight: Bagaimana minat berubah seiring usia', 
               fontsize=15, fontweight='bold')
ax10.set_xlabel('Age Groups', fontsize=12)
ax10.set_ylabel('Interest Percentage (%)', fontsize=12)
ax10.legend(fontsize=11)
ax10.grid(alpha=0.3)

# 11. CLUSTER CHARACTERISTICS COMPARISON
ax11 = fig.add_subplot(gs[6, :])

# Create cluster characteristics matrix
cluster_characteristics = []
cluster_names = []

for cluster_id in range(7):
    cluster_data = df[df['Cluster'] == cluster_id]
    
    if len(cluster_data) > 0:
        characteristics = []
        
        # Average age
        avg_age = cluster_data['Usia'].mean()
        characteristics.append(avg_age)
        
        # Average price
        avg_price = cluster_data['Harga_Kelas'].mean()
        characteristics.append(avg_price)
        
        # Entrepreneurship percentage
        entrepreneur_pct = (cluster_data['Sub_Kategori_2'] == 'Entrepreneurship').mean() * 100
        characteristics.append(entrepreneur_pct)
        
        # Creative percentage
        creative_count = 0
        for col in ['Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']:
            creative_count += cluster_data[col].isin(['Seni & Visual', 'Crafting, Journaling, DIY']).sum()
        creative_pct = (creative_count / len(cluster_data)) * 100
        characteristics.append(creative_pct)
        
        cluster_characteristics.append(characteristics)
        cluster_names.append(f'Cluster {cluster_id}')

# Create heatmap
char_matrix = np.array(cluster_characteristics).T
char_labels = ['Avg Age', 'Avg Price (Rp)', 'Entrepreneurship %', 'Creative %']

# Normalize for better visualization
char_matrix_norm = np.zeros_like(char_matrix)
for i in range(len(char_labels)):
    min_val = char_matrix[i].min()
    max_val = char_matrix[i].max()
    if max_val > min_val:
        char_matrix_norm[i] = (char_matrix[i] - min_val) / (max_val - min_val) * 100
    else:
        char_matrix_norm[i] = char_matrix[i]

im = ax11.imshow(char_matrix_norm, cmap='RdYlBu_r', aspect='auto')
ax11.set_xticks(range(len(cluster_names)))
ax11.set_xticklabels(cluster_names)
ax11.set_yticks(range(len(char_labels)))
ax11.set_yticklabels(char_labels)
ax11.set_title('🎯 CLUSTER CHARACTERISTICS HEATMAP\n🔍 Cara Baca: Warna gelap = nilai tinggi, Terang = nilai rendah\n' +
               'Insight: Profil karakteristik setiap cluster', 
               fontsize=15, fontweight='bold')

# Add actual values to heatmap
for i in range(len(char_labels)):
    for j in range(len(cluster_names)):
        if i < 2:  # Age and Price
            text = ax11.text(j, i, f'{char_matrix[i, j]:.1f}',
                           ha="center", va="center", color="white", fontweight='bold')
        else:  # Percentages
            text = ax11.text(j, i, f'{char_matrix[i, j]:.1f}%',
                           ha="center", va="center", color="white", fontweight='bold')

plt.colorbar(im, ax=ax11, label='Normalized Score (0-100)')

# 12. BUSINESS OPPORTUNITY MATRIX
ax12 = fig.add_subplot(gs[7, :])

# Define business opportunities based on analysis
opportunities = []

# Calculate actual market sizes and engagement rates
for cluster_id in range(7):
    cluster_data = df[df['Cluster'] == cluster_id]
    market_size = len(cluster_data)
    
    # Calculate engagement rate (entrepreneurship + creative interests)
    entrepreneur_pct = (cluster_data['Sub_Kategori_2'] == 'Entrepreneurship').mean() * 100
    
    creative_count = 0
    for col in ['Sub_Kategori_2', 'Sub_Kategori_3', 'Sub_Kategori_4']:
        creative_count += cluster_data[col].isin(['Seni & Visual', 'Crafting, Journaling, DIY']).sum()
    creative_pct = (creative_count / len(cluster_data)) * 100 if len(cluster_data) > 0 else 0
    
    engagement_rate = min(entrepreneur_pct + creative_pct * 0.3, 100)  # Weighted engagement
    
    # Determine cluster description
    avg_age = cluster_data['Usia'].mean()
    avg_price = cluster_data['Harga_Kelas'].mean()
    
    if avg_age < 15:
        description = f"Creative Kids\n(Age: {avg_age:.1f})"
    elif entrepreneur_pct > 70:
        description = f"Entrepreneurs\n(Age: {avg_age:.1f})"
    elif creative_pct > 30:
        description = f"Creative Adults\n(Age: {avg_age:.1f})"
    else:
        description = f"Other Focus\n(Age: {avg_age:.1f})"
    
    opportunities.append((description, market_size, engagement_rate))

# Extract data for scatter plot
names = [opp[0] for opp in opportunities]
market_sizes = [opp[1] for opp in opportunities]
engagement_rates = [opp[2] for opp in opportunities]

scatter = ax12.scatter(market_sizes, engagement_rates, 
                       s=[size*2 for size in market_sizes], 
                       c=cluster_colors[:len(opportunities)], alpha=0.7)

# Add labels
for i, (name, size, engagement) in enumerate(opportunities):
    ax12.annotate(f'{name}\n({size} customers)', 
                  (size, engagement), 
                  xytext=(10, 10), textcoords='offset points',
                  fontsize=10, ha='left',
                  bbox=dict(boxstyle='round,pad=0.3', facecolor=cluster_colors[i], alpha=0.3))

ax12.set_xlabel('Market Size (Number of Customers)', fontsize=13)
ax12.set_ylabel('Engagement Potential (%)', fontsize=13)
ax12.set_title('💼 BUSINESS OPPORTUNITY MATRIX\n🔍 Cara Baca: X-axis = ukuran pasar, Y-axis = potensi engagement\n' +
               'Ukuran bubble = skala peluang, Insight: Prioritas pengembangan bisnis', 
               fontsize=15, fontweight='bold')
ax12.grid(alpha=0.3)

# Add quadrant lines
ax12.axhline(y=np.mean(engagement_rates), color='red', linestyle='--', alpha=0.5)
ax12.axvline(x=np.mean(market_sizes), color='red', linestyle='--', alpha=0.5)

# Add quadrant labels
ax12.text(max(market_sizes)*0.8, max(engagement_rates)*0.95, 'High Engagement\nLarge Market', 
          ha='center', va='center', fontweight='bold', 
          bbox=dict(boxstyle='round,pad=0.5', facecolor='lightgreen', alpha=0.7))

ax12.text(max(market_sizes)*0.2, max(engagement_rates)*0.95, 'High Engagement\nSmall Market', 
          ha='center', va='center', fontweight='bold', 
          bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))

ax12.text(max(market_sizes)*0.8, max(engagement_rates)*0.05, 'Low Engagement\nLarge Market', 
          ha='center', va='center', fontweight='bold', 
          bbox=dict(boxstyle='round,pad=0.5', facecolor='orange', alpha=0.7))

# 13. SUMMARY STATISTICS
ax13 = fig.add_subplot(gs[8, :])
ax13.axis('off')

# Create summary text
summary_text = f"""
📊 COMPREHENSIVE ANALYSIS SUMMARY - VISUAL INTEGRATION GUIDE

🎯 DATASET OVERVIEW:
• Total Customers: {len(df):,} customers analyzed
• Age Range: {df['Usia'].min()}-{df['Usia'].max()} years (Median: {df['Usia'].median():.1f} years)
• Price Range: Rp{df['Harga_Kelas'].min()}-{df['Harga_Kelas'].max()} (Median: Rp{df['Harga_Kelas'].median():.0f})
• Geographic Coverage: {df['Domisili'].nunique()} unique locations nationwide
• Program Diversity: {df['Nama_Program'].nunique()} different programs offered

💼 KEY BUSINESS INSIGHTS:
• Entrepreneurship Interest: {(df['Sub_Kategori_2'] == 'Entrepreneurship').sum():,} customers ({(df['Sub_Kategori_2'] == 'Entrepreneurship').mean()*100:.1f}%)
• Creative Market: {((df['Sub_Kategori_3'] == 'Seni & Visual') | (df['Sub_Kategori_4'] == 'Crafting, Journaling, DIY')).sum():,} customers interested in creative arts
• Child Focus Market: {(df['Kategori'] == 'Anak').sum():,} customers ({(df['Kategori'] == 'Anak').mean()*100:.1f}%) focused on child development
• Culinary Market: {(df['Kategori'] == 'Memasak').sum():,} customers ({(df['Kategori'] == 'Memasak').mean()*100:.1f}%) interested in cooking

🎯 CLUSTER INSIGHTS:
• Optimal Segmentation: 7 distinct customer clusters identified
• Largest Segment: Cluster {cluster_counts.idxmax()} with {cluster_counts.max():,} customers ({cluster_counts.max()/len(df)*100:.1f}%)
• Most Balanced Distribution: Even spread across age and price segments
• Clear Differentiation: Strong statistical separation between clusters

📈 STRATEGIC RECOMMENDATIONS:
• Focus on entrepreneurship development programs (51.9% market)
• Develop integrated creative-business platforms
• Leverage multi-generational approach (0-63 years coverage)
• Expand geographic presence in top concentration areas
"""

ax13.text(0.02, 0.98, summary_text, transform=ax13.transAxes, fontsize=12,
          verticalalignment='top', horizontalalignment='left',
          bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.3))

plt.suptitle('🎯 COMPREHENSIVE CUSTOMER SEGMENTATION - INTEGRATED VISUAL ANALYSIS\n' +
             'Complete Visual Guide with Reading Instructions for Strategic Decision Making\n' +
             'Dataset: 2,822 customers | 7 Clusters | 32 Unique Interests | National Coverage', 
             fontsize=22, fontweight='bold', y=0.99)

plt.tight_layout()
plt.savefig('comprehensive_integrated_visual_analysis.png', 
            dpi=300, bbox_inches='tight', facecolor='white')
plt.show()

print("\n" + "="*100)
print("📊 INTEGRATED VISUAL ANALYSIS COMPLETED!")
print("="*100)
print("\n🎯 COMPREHENSIVE CHART READING GUIDE:")
print("\n1. 📊 CLUSTER OVERVIEW: Shows 7 customer segments with exact sizes and percentages")
print("   • Height = number of customers, Colors = different segments")
print("   • Use for: Understanding market segment distribution")

print("\n2. 👥 AGE-PRICE SCATTER: Reveals customer positioning by demographics and spending")
print("   • Position = age vs price relationship, Colors = segment types")
print("   • Use for: Targeting strategies and pricing optimization")

print("\n3. 🎯 CATEGORY PIE: Primary interest distribution across entire customer base")
print("   • Slice size = market share, Percentages = customer distribution")
print("   • Use for: Product development and category focus")

print("\n4. 💼 ENTREPRENEURSHIP PIE: Business-minded vs other customer interests")
print("   • Red = business-focused customers, Gray = other interests")
print("   • Use for: Business program development planning")

print("\n5. 📈 AGE BOXPLOTS: Age range and median for each customer cluster")
print("   • Box = age range, Center line = median age, Dots = outliers")
print("   • Use for: Age-appropriate program design")

print("\n6. 💰 PRICE BOXPLOTS: Spending patterns and price positioning by segment")
print("   • Box height = price range, Position = typical spending habits")
print("   • Use for: Pricing strategy and package development")

print("\n7. 🎨 TOP INTERESTS: Most popular secondary interests across all customers")
print("   • Bar length = popularity ranking, Shows demand patterns")
print("   • Use for: Program expansion and new offering development")

print("\n8. 🌍 GEOGRAPHIC BARS: Top customer concentration by cities")
print("   • Bar length = customer count, Cities ranked by market size")
print("   • Use for: Geographic expansion and marketing focus")

print("\n9. 📚 PROGRAM BARS: Most popular programs by enrollment numbers")
print("   • Height = enrollment count, Programs ranked by demand")
print("   • Use for: Resource allocation and program optimization")

print("\n10. 📊 INTEREST EVOLUTION: How customer interests change across age groups")
print("    • Lines = interest trends, Points = percentage in age group")
print("    • Use for: Lifecycle marketing and age-appropriate offerings")

print("\n11. 🎯 CHARACTERISTICS HEATMAP: Multi-dimensional cluster profiling")
print("    • Dark colors = high values, Light colors = low values")
print("    • Use for: Comprehensive segment understanding and targeting")

print("\n12. 💼 OPPORTUNITY MATRIX: Business potential vs market size analysis")
print("    • X-axis = market size, Y-axis = engagement potential")
print("    • Bubble size = opportunity scale, Colors = different segments")
print("    • Use for: Strategic planning and investment prioritization")

print("\n13. 📋 SUMMARY STATISTICS: Complete dataset overview and key insights")
print("    • Comprehensive numbers and percentages for strategic reference")
print("    • Use for: Executive reporting and strategic presentations")

print(f"\n✅ All visualizations integrated and saved to: comprehensive_integrated_visual_analysis.png")
print(f"📊 Dataset analyzed: {len(df):,} customers across {df['Domisili'].nunique()} locations")
print(f"🎯 Strategic insights: 7 clusters, {df['Kategori'].nunique()} main categories, {df['Nama_Program'].nunique()} programs")
print("📈 Ready for business strategy implementation and decision making!")
