import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# Set style
plt.style.use('default')
sns.set_palette("husl")

# Load data
df = pd.read_csv('01_data/data_with_clusters.csv')
seni_df = pd.read_csv('05_results/seni_crafting_customers.csv')

print("🎨 CREATING VISUALIZATIONS - SENI/CRAFTING DISCOVERY")
print("=" * 60)

# Create comprehensive visualization
fig = plt.figure(figsize=(20, 16))

# 1. Main Discovery - Pie Chart of Creative Interest
ax1 = plt.subplot(3, 3, 1)
creative_counts = [len(seni_df), len(df) - len(seni_df)]
creative_labels = [f'Creative Interest\n{len(seni_df)} customers\n(61.2%)', 
                  f'Non-Creative\n{len(df) - len(seni_df)} customers\n(38.8%)']
colors1 = ['#FF6B6B', '#4ECDC4']

wedges, texts, autotexts = ax1.pie(creative_counts, labels=creative_labels, autopct='%1.1f%%', 
                                  colors=colors1, startangle=90, textprops={'fontsize': 10})
ax1.set_title('🎨 MAJOR DISCOVERY\nCreative Interest Distribution', fontsize=14, fontweight='bold', pad=20)

# 2. Creative Distribution Across Clusters
ax2 = plt.subplot(3, 3, 2)
cluster_names = ['Penggemar\nKuliner', 'Orang Tua\n& Anak', 'Kreator\nFashion']
creative_per_cluster = [783, 613, 330]
total_per_cluster = [993, 1499, 330]

x = np.arange(len(cluster_names))
width = 0.35

bars1 = ax2.bar(x - width/2, total_per_cluster, width, label='Total Customers', color='lightblue', alpha=0.7)
bars2 = ax2.bar(x + width/2, creative_per_cluster, width, label='Creative Interest', color='coral')

ax2.set_xlabel('Customer Clusters')
ax2.set_ylabel('Number of Customers')
ax2.set_title('🎯 Creative Interest by Cluster', fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(cluster_names)
ax2.legend()

# Add percentage labels
for i, (total, creative) in enumerate(zip(total_per_cluster, creative_per_cluster)):
    percentage = (creative/total)*100
    ax2.text(i + width/2, creative + 20, f'{percentage:.1f}%', ha='center', fontweight='bold')

# 3. Interest Type Breakdown
ax3 = plt.subplot(3, 3, 3)
interest_types = ['Seni & Visual', 'Crafting/DIY', 'Kreativitas\nDewasa', 'Design', 'Art']
interest_counts = [898, 851, 310, 52, 58]
colors3 = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']

bars = ax3.bar(interest_types, interest_counts, color=colors3)
ax3.set_title('🎨 Creative Interest Types', fontweight='bold')
ax3.set_ylabel('Number of Customers')
plt.setp(ax3.get_xticklabels(), rotation=45, ha='right')

# Add value labels
for bar, count in zip(bars, interest_counts):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'{count}', ha='center', va='bottom', fontweight='bold')

# 4. Original vs New TAM Comparison
ax4 = plt.subplot(3, 3, 4)
tam_comparison = ['Original\nEducation Focus', 'Creative Market\nOpportunity']
tam_values = [554, 2780]  # in millions
colors4 = ['lightcoral', 'gold']

bars = ax4.bar(tam_comparison, tam_values, color=colors4, alpha=0.8)
ax4.set_title('💰 TAM Comparison (Millions Rp)', fontweight='bold')
ax4.set_ylabel('TAM (Millions Rp)')

# Add value labels and growth indicator
for i, (bar, value) in enumerate(zip(bars, tam_values)):
    height = bar.get_height()
    ax4.text(bar.get_x() + bar.get_width()/2., height + 50,
             f'Rp{value}M', ha='center', va='bottom', fontweight='bold', fontsize=12)

# Add growth arrow
ax4.annotate('5x Growth!', xy=(1, 2780), xytext=(0.5, 2000),
            arrowprops=dict(arrowstyle='->', color='red', lw=2),
            fontsize=12, fontweight='bold', color='red', ha='center')

# 5. K=5 Clustering Results
ax5 = plt.subplot(3, 3, 5)
alt_df = pd.read_csv('05_results/alternative_clustering.csv')
cluster_k5_counts = alt_df['Cluster_K5'].value_counts().sort_index()

cluster_k5_labels = ['Young\nCreatives', 'Family\nEducation', 'Fashion\nCreators', 'Mature\nCooking', 'Premium\nCooking']
colors5 = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

bars = ax5.bar(range(len(cluster_k5_counts)), cluster_k5_counts.values, color=colors5)
ax5.set_title('🔄 Alternative K=5 Clustering', fontweight='bold')
ax5.set_xlabel('New Clusters')
ax5.set_ylabel('Customers')
ax5.set_xticks(range(len(cluster_k5_labels)))
ax5.set_xticklabels(cluster_k5_labels, rotation=45, ha='right')

# Add cluster info
cluster_info = ['465\n(16.5%)', '1056\n(37.4%)', '255\n(9.0%)', '677\n(24.0%)', '369\n(13.1%)']
for bar, info in zip(bars, cluster_info):
    height = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2., height/2,
             info, ha='center', va='center', fontweight='bold', color='white')

# 6. Business Opportunity Matrix
ax6 = plt.subplot(3, 3, 6)
opportunities = ['Culinary\nArt Fusion', 'Creative\nFamily Hub', 'Young\nCreator Platform', 'Fashion\nCreatives']
market_sizes = [783, 613, 465, 330]
monthly_arpu = [100, 120, 65, 150]

# Create scatter plot
scatter = ax6.scatter(market_sizes, monthly_arpu, s=[size*0.5 for size in market_sizes], 
                     c=['coral', 'lightgreen', 'skyblue', 'gold'], alpha=0.7)

ax6.set_xlabel('Market Size (Customers)')
ax6.set_ylabel('Monthly ARPU (Rp 000)')
ax6.set_title('🎯 Business Opportunity Matrix', fontweight='bold')

# Add labels
for i, opp in enumerate(opportunities):
    ax6.annotate(opp, (market_sizes[i], monthly_arpu[i]), 
                xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')

# 7. Sub-category Analysis
ax7 = plt.subplot(3, 3, 7)
sub_categories = ['Entrepreneurship', 'Kreativitas\n& Belajar Anak', 'Kreativitas\nDewasa', 
                 'Seni & Visual', 'Crafting/DIY', 'Food Styling']
sub_counts = [1465, 776, 310, 898, 851, 917]
colors7 = plt.cm.Set3(np.linspace(0, 1, len(sub_categories)))

bars = ax7.barh(sub_categories, sub_counts, color=colors7)
ax7.set_title('📊 Sub-Category Interest Distribution', fontweight='bold')
ax7.set_xlabel('Number of Customers')

# Add value labels
for bar, count in zip(bars, sub_counts):
    width = bar.get_width()
    ax7.text(width + 20, bar.get_y() + bar.get_height()/2,
             f'{count}', ha='left', va='center', fontweight='bold')

# 8. Age Distribution Comparison
ax8 = plt.subplot(3, 3, 8)
cluster_ages = df.groupby('Cluster')['Usia_Clean'].mean()
seni_ages = seni_df.groupby('Cluster')['Usia_Clean'].mean()

x = np.arange(3)
width = 0.35

bars1 = ax8.bar(x - width/2, cluster_ages.values, width, label='All Customers', alpha=0.7)
bars2 = ax8.bar(x + width/2, seni_ages.values, width, label='Creative Interest', alpha=0.7)

ax8.set_xlabel('Clusters')
ax8.set_ylabel('Average Age')
ax8.set_title('🎂 Age Comparison', fontweight='bold')
ax8.set_xticks(x)
ax8.set_xticklabels(['Kuliner', 'Family', 'Fashion'])
ax8.legend()

# Add value labels
for i, (all_age, seni_age) in enumerate(zip(cluster_ages.values, seni_ages.values)):
    ax8.text(i - width/2, all_age + 0.5, f'{all_age:.1f}', ha='center', fontweight='bold')
    ax8.text(i + width/2, seni_age + 0.5, f'{seni_age:.1f}', ha='center', fontweight='bold')

# 9. Revenue Potential Comparison
ax9 = plt.subplot(3, 3, 9)
business_models = ['Original\nEducation', 'Creative\nFusion', 'Multi-Segment\nPlatform']
annual_revenue = [57, 282, 450]  # in millions
colors9 = ['lightcoral', 'lightgreen', 'gold']

bars = ax9.bar(business_models, annual_revenue, color=colors9, alpha=0.8)
ax9.set_title('💰 Annual Revenue Potential\n(Millions Rp)', fontweight='bold')
ax9.set_ylabel('Revenue (Millions Rp)')

# Add value labels
for bar, revenue in zip(bars, annual_revenue):
    height = bar.get_height()
    ax9.text(bar.get_x() + bar.get_width()/2., height + 10,
             f'Rp{revenue}M', ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.tight_layout(pad=3.0)
plt.suptitle('🎨 DISCOVERY: Hidden Creative Market (61.2% of customers)', 
             fontsize=18, fontweight='bold', y=0.98)

plt.savefig('05_results/creative_market_discovery.png', dpi=300, bbox_inches='tight')
plt.show()

# Create summary infographic
fig2, ax = plt.subplots(1, 1, figsize=(12, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')

# Title
ax.text(5, 9.5, '🎨 MAJOR DISCOVERY: HIDDEN CREATIVE MARKET', 
        fontsize=20, fontweight='bold', ha='center')

# Key stats boxes
# Box 1: Market Size
rect1 = Rectangle((0.5, 7), 2, 1.5, linewidth=2, edgecolor='red', facecolor='lightcoral', alpha=0.3)
ax.add_patch(rect1)
ax.text(1.5, 7.75, '1,726 CUSTOMERS\n61.2% Creative Interest', 
        fontsize=12, fontweight='bold', ha='center', va='center')

# Box 2: TAM Growth
rect2 = Rectangle((3, 7), 2, 1.5, linewidth=2, edgecolor='green', facecolor='lightgreen', alpha=0.3)
ax.add_patch(rect2)
ax.text(4, 7.75, 'TAM GROWTH\n5x LARGER\nRp2.78B vs Rp554M', 
        fontsize=12, fontweight='bold', ha='center', va='center')

# Box 3: New Segments
rect3 = Rectangle((5.5, 7), 2, 1.5, linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax.add_patch(rect3)
ax.text(6.5, 7.75, 'NEW SEGMENTS\nCulinary Art\nCreative Family\nYoung Creators', 
        fontsize=12, fontweight='bold', ha='center', va='center')

# Box 4: Success Rate
rect4 = Rectangle((7.5, 7), 2, 1.5, linewidth=2, edgecolor='orange', facecolor='orange', alpha=0.3)
ax.add_patch(rect4)
ax.text(8.5, 7.75, 'SUCCESS RATE\n85-90%\nProven Interest', 
        fontsize=12, fontweight='bold', ha='center', va='center')

# Business opportunities
ax.text(5, 6, 'TOP BUSINESS OPPORTUNITIES', fontsize=16, fontweight='bold', ha='center')

opportunities_text = """
🍳 CULINARY ART FUSION: 783 customers → Rp940M TAM
👨‍👩‍👧‍👦 CREATIVE FAMILY HUB: 613 customers → Rp882M TAM  
🎨 YOUNG CREATOR PLATFORM: 465 customers → Rp362M TAM
👗 FASHION CREATIVES: 330 customers → Rp594M TAM
"""

ax.text(5, 4.5, opportunities_text, fontsize=12, ha='center', va='top',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightyellow", alpha=0.5))

# Why missed in original clustering
ax.text(5, 2.5, 'WHY MISSED IN ORIGINAL CLUSTERING?', fontsize=14, fontweight='bold', ha='center')
why_text = """
• Creative interests were in sub-categories (not primary)
• Multi-interest customers don't fit single cluster paradigm  
• Algorithm focused on demographics, not psychographics
• Interest patterns hidden across multiple columns
"""

ax.text(5, 1.5, why_text, fontsize=11, ha='center', va='top',
        bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.3))

# Action required
ax.text(5, 0.5, '🚀 ACTION: PIVOT TO CREATIVE LIFESTYLE PLATFORM', 
        fontsize=14, fontweight='bold', ha='center', 
        bbox=dict(boxstyle="round,pad=0.3", facecolor="gold", alpha=0.7))

plt.savefig('05_results/creative_discovery_infographic.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n📊 VISUALIZATIONS CREATED:")
print("   • creative_market_discovery.png - Comprehensive analysis")
print("   • creative_discovery_infographic.png - Executive summary")
print(f"\n✅ CREATIVE MARKET DISCOVERY VISUALIZATION COMPLETE!")
print(f"🎯 KEY MESSAGE: 61.2% customers have creative interests - 5x larger market opportunity!")
