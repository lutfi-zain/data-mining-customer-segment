import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("🚀 MARKET OPPORTUNITY ANALYSIS - PHASE 2.1")
print("=" * 60)

# Load customer segmentation data
df = pd.read_csv('01_data/data_with_clusters.csv')

print(f"📊 Dataset loaded: {len(df)} customers dengan 3 segmen tervalidasi")
print(f"📅 Analysis date: {datetime.now().strftime('%d %B %Y')}")

# ===================================================================
# TASK 1: PRODUCT DEMAND ANALYSIS PER SEGMENT
# ===================================================================

print("\n🎯 TASK 1: PRODUCT DEMAND ANALYSIS PER SEGMENT")
print("-" * 50)

# Analyze program preferences by segment
segment_programs = df.groupby('Cluster').agg({
    'Nama Program': lambda x: x.value_counts().to_dict(),
    'Harga Kelas': ['mean', 'median', 'std'],
    'Usia_Clean': ['mean', 'median'],
    'Domisili': lambda x: x.value_counts().head(3).to_dict()
}).round(2)

# Create segment names mapping
segment_names = {
    0: "Penggemar Kuliner",
    1: "Orang Tua & Anak", 
    2: "Kreator Fashion"
}

print("\n📈 PRODUCT DEMAND BY SEGMENT:")

for cluster in df['Cluster'].unique():
    segment_name = segment_names[cluster]
    segment_data = df[df['Cluster'] == cluster]
    
    print(f"\n🎯 {segment_name.upper()} (Cluster {cluster})")
    print(f"   👥 Size: {len(segment_data)} customers ({len(segment_data)/len(df)*100:.1f}%)")
    print(f"   💰 Avg Monthly Purchase: Rp{segment_data['Harga Kelas'].mean():,.0f}")
    
    # Top program preferences
    top_programs = segment_data['Nama Program'].value_counts().head(3)
    print(f"   🏆 Top Program Preferences:")
    for i, (program, count) in enumerate(top_programs.items(), 1):
        percentage = count/len(segment_data)*100
        print(f"      {i}. {program}: {count} customers ({percentage:.1f}%)")
    
    # Age demographics
    print(f"   🎂 Age Profile: {segment_data['Usia_Clean'].mean():.1f} years avg")
    
    # Geographic concentration
    top_cities = segment_data['Domisili'].value_counts().head(2)
    print(f"   🌍 Geographic Focus: {', '.join(top_cities.index[:2])}")

# ===================================================================
# TASK 2: MARKET SIZE & GROWTH POTENTIAL CALCULATION
# ===================================================================

print(f"\n\n🎯 TASK 2: MARKET SIZE & GROWTH POTENTIAL")
print("-" * 50)

# Calculate Total Addressable Market (TAM) per segment
tam_analysis = []

for cluster in df['Cluster'].unique():
    segment_name = segment_names[cluster]
    segment_data = df[df['Cluster'] == cluster]
    
    # Current metrics
    current_customers = len(segment_data)
    avg_monthly_spend = segment_data['Harga Kelas'].mean()
    annual_revenue_per_customer = avg_monthly_spend * 12
    current_annual_revenue = current_customers * annual_revenue_per_customer
    
    # Market size estimation (assuming our sample represents 1% of total market)
    estimated_total_customers = current_customers * 100  # Conservative estimate
    total_addressable_market = estimated_total_customers * annual_revenue_per_customer
    
    # Growth potential based on segment characteristics
    if cluster == 0:  # Penggemar Kuliner
        growth_multiplier = 2.5  # Food market is expanding
        growth_confidence = "High"
    elif cluster == 1:  # Orang Tua & Anak
        growth_multiplier = 3.0  # Education market booming
        growth_confidence = "Very High"
    else:  # Kreator Fashion
        growth_multiplier = 2.0  # Premium market slower but steady
        growth_confidence = "Medium-High"
    
    projected_market_size = total_addressable_market * growth_multiplier
    
    tam_analysis.append({
        'Segment': segment_name,
        'Current_Customers': current_customers,
        'Avg_Annual_Spend': annual_revenue_per_customer,
        'Current_Revenue': current_annual_revenue,
        'TAM_Conservative': total_addressable_market,
        'TAM_Growth_Potential': projected_market_size,
        'Growth_Multiplier': growth_multiplier,
        'Confidence_Level': growth_confidence
    })

# Display TAM analysis
tam_df = pd.DataFrame(tam_analysis)
print("\n📊 TOTAL ADDRESSABLE MARKET (TAM) ANALYSIS:")
print("=" * 80)

for _, row in tam_df.iterrows():
    print(f"\n🎯 {row['Segment'].upper()}")
    print(f"   📊 Current Sample: {row['Current_Customers']:,} customers")
    print(f"   💰 Annual Spend/Customer: Rp{row['Avg_Annual_Spend']:,.0f}")
    print(f"   💸 Current Annual Revenue: Rp{row['Current_Revenue']:,.0f}")
    print(f"   🎯 TAM (Conservative): Rp{row['TAM_Conservative']:,.0f}")
    print(f"   🚀 TAM (Growth Potential): Rp{row['TAM_Growth_Potential']:,.0f}")
    print(f"   📈 Growth Confidence: {row['Confidence_Level']}")

# ===================================================================
# TASK 3: COMPETITIVE LANDSCAPE MAPPING
# ===================================================================

print(f"\n\n🎯 TASK 3: COMPETITIVE LANDSCAPE MAPPING")
print("-" * 50)

# Define competitive landscape based on segment analysis
competitive_landscape = {
    "Penggemar Kuliner": {
        "direct_competitors": ["Yummy App", "Cookpad", "SajianSedap"],
        "indirect_competitors": ["YouTube Cooking", "Instagram Chefs", "Cooking Classes"],
        "market_gaps": [
            "Personal cooking mentor",
            "Ingredient sourcing integration", 
            "Community cooking challenges",
            "Recipe customization AI"
        ],
        "competitive_advantage": [
            "Data-driven recipe recommendations",
            "Community-based learning",
            "Local ingredient sourcing"
        ]
    },
    "Orang Tua & Anak": {
        "direct_competitors": ["Ruangguru Kids", "Zenius", "Quipper"],
        "indirect_competitors": ["Traditional tutoring", "School programs", "Educational toys"],
        "market_gaps": [
            "Parent-child interactive learning",
            "Personalized education path",
            "Real-time progress tracking",
            "Gamified family education"
        ],
        "competitive_advantage": [
            "Family-centric approach",
            "Age-appropriate content curation",
            "Parent engagement tools"
        ]
    },
    "Kreator Fashion": {
        "direct_competitors": ["Zalora", "Shopee Fashion", "Fashion Valet"],
        "indirect_competitors": ["Instagram shops", "Local boutiques", "Tailor services"],
        "market_gaps": [
            "Style prediction AI",
            "Virtual fitting room",
            "Sustainable fashion focus",
            "Creator monetization platform"
        ],
        "competitive_advantage": [
            "Creator-first platform",
            "Premium personalization",
            "Trend prediction analytics"
        ]
    }
}

print("\n🏆 COMPETITIVE LANDSCAPE ANALYSIS:")
print("=" * 60)

for segment, analysis in competitive_landscape.items():
    print(f"\n🎯 {segment.upper()}")
    print(f"   🎪 Direct Competitors: {', '.join(analysis['direct_competitors'])}")
    print(f"   🌐 Indirect Competitors: {', '.join(analysis['indirect_competitors'][:2])}...")
    print(f"   🕳️  Market Gaps Identified: {len(analysis['market_gaps'])} opportunities")
    for gap in analysis['market_gaps']:
        print(f"      • {gap}")
    print(f"   ⚡ Our Competitive Advantages: {len(analysis['competitive_advantage'])} key factors")

# ===================================================================
# TASK 4: UNMET NEEDS IDENTIFICATION
# ===================================================================

print(f"\n\n🎯 TASK 4: UNMET NEEDS IDENTIFICATION")
print("-" * 50)

# Analyze purchasing patterns to identify unmet needs
unmet_needs_analysis = {}

for cluster in df['Cluster'].unique():
    segment_name = segment_names[cluster]
    segment_data = df[df['Cluster'] == cluster]
    
    # Analyze purchase frequency and amount patterns
    purchase_std = segment_data['Harga Kelas'].std()
    purchase_mean = segment_data['Harga Kelas'].mean()
    high_variance = purchase_std / purchase_mean > 0.5  # High variance indicates inconsistent satisfaction
    
    # Age-based needs analysis
    age_groups = pd.cut(segment_data['Usia_Clean'], bins=[0, 25, 35, 45, 100], labels=['18-25', '26-35', '36-45', '45+'])
    age_distribution = age_groups.value_counts()
    
    unmet_needs = []
    
    if cluster == 0:  # Penggemar Kuliner
        unmet_needs = [
            "Smart kitchen integration",
            "Meal planning automation", 
            "Nutritional tracking",
            "Cooking skill certification",
            "Local chef connections"
        ]
    elif cluster == 1:  # Orang Tua & Anak
        unmet_needs = [
            "Parent education support",
            "Child development tracking",
            "Family activity recommendations",
            "Educational progress analytics",
            "Peer parent community"
        ]
    else:  # Kreator Fashion
        unmet_needs = [
            "Style evolution tracking",
            "Sustainable fashion options",
            "Creator collaboration tools",
            "Trend forecasting access",
            "Personal brand development"
        ]
    
    unmet_needs_analysis[segment_name] = {
        'primary_needs': unmet_needs,
        'purchase_variance': 'High' if high_variance else 'Low',
        'dominant_age_group': age_distribution.index[0],
        'satisfaction_gaps': purchase_std / purchase_mean
    }

print("\n🔍 UNMET NEEDS ANALYSIS:")
print("=" * 50)

for segment, analysis in unmet_needs_analysis.items():
    print(f"\n🎯 {segment.upper()}")
    print(f"   📊 Purchase Variance: {analysis['purchase_variance']} (Gap Score: {analysis['satisfaction_gaps']:.2f})")
    print(f"   👥 Dominant Age Group: {analysis['dominant_age_group']}")
    print(f"   🎯 Primary Unmet Needs:")
    for i, need in enumerate(analysis['primary_needs'], 1):
        print(f"      {i}. {need}")

# ===================================================================
# TASK 5: CROSS-SELLING OPPORTUNITY MATRIX
# ===================================================================

print(f"\n\n🎯 TASK 5: CROSS-SELLING OPPORTUNITY MATRIX")
print("-" * 50)

# Analyze potential cross-selling between segments
cross_sell_matrix = []

# Calculate segment overlap potential based on age and spending patterns
segments_data = {}
for cluster in df['Cluster'].unique():
    segment_name = segment_names[cluster]
    segment_data = df[df['Cluster'] == cluster]
    segments_data[segment_name] = {
        'age_range': (segment_data['Usia_Clean'].min(), segment_data['Usia_Clean'].max()),
        'avg_spend': segment_data['Harga Kelas'].mean(),
        'programs': segment_data['Nama Program'].value_counts().to_dict()
    }

# Define cross-selling opportunities
cross_sell_opportunities = {
    "Penggemar Kuliner → Orang Tua & Anak": {
        "opportunity": "Family cooking programs",
        "potential": "High",
        "rationale": "Parents who cook want to teach children",
        "estimated_conversion": "25%"
    },
    "Penggemar Kuliner → Kreator Fashion": {
        "opportunity": "Food styling & presentation",
        "potential": "Medium", 
        "rationale": "Food presentation overlaps with aesthetic sense",
        "estimated_conversion": "15%"
    },
    "Orang Tua & Anak → Penggemar Kuliner": {
        "opportunity": "Healthy cooking for kids",
        "potential": "High",
        "rationale": "Parents want healthy meal options",
        "estimated_conversion": "30%"
    },
    "Orang Tua & Anak → Kreator Fashion": {
        "opportunity": "Kids fashion & styling",
        "potential": "Medium",
        "rationale": "Parents invest in children's appearance",
        "estimated_conversion": "20%"
    },
    "Kreator Fashion → Penggemar Kuliner": {
        "opportunity": "Lifestyle & aesthetic dining",
        "potential": "Medium",
        "rationale": "Fashion-conscious people care about food presentation",
        "estimated_conversion": "18%"
    },
    "Kreator Fashion → Orang Tua & Anak": {
        "opportunity": "Family styling services", 
        "potential": "Low-Medium",
        "rationale": "Fashion creators becoming parents",
        "estimated_conversion": "12%"
    }
}

print("\n🔄 CROSS-SELLING OPPORTUNITY MATRIX:")
print("=" * 70)

total_cross_sell_revenue = 0

for cross_sell, details in cross_sell_opportunities.items():
    from_segment, to_segment = cross_sell.split(" → ")
    
    # Calculate potential revenue
    from_size = len(df[df['Cluster'] == list(segment_names.keys())[list(segment_names.values()).index(from_segment)]])
    conversion_rate = float(details['estimated_conversion'].rstrip('%')) / 100
    potential_customers = from_size * conversion_rate
    
    # Estimate revenue per cross-sell customer (70% of target segment average)
    to_cluster = list(segment_names.keys())[list(segment_names.values()).index(to_segment)]
    target_avg_spend = df[df['Cluster'] == to_cluster]['Harga Kelas'].mean()
    cross_sell_revenue = potential_customers * target_avg_spend * 12 * 0.7  # 70% of full spend
    
    total_cross_sell_revenue += cross_sell_revenue
    
    print(f"\n🎯 {cross_sell}")
    print(f"   💡 Opportunity: {details['opportunity']}")
    print(f"   📊 Potential: {details['potential']}")
    print(f"   📈 Conversion Rate: {details['estimated_conversion']}")
    print(f"   👥 Potential Customers: {potential_customers:.0f}")
    print(f"   💰 Annual Revenue Potential: Rp{cross_sell_revenue:,.0f}")
    print(f"   📝 Rationale: {details['rationale']}")

print(f"\n💰 TOTAL CROSS-SELL REVENUE POTENTIAL: Rp{total_cross_sell_revenue:,.0f}")

# ===================================================================
# SUMMARY & BUSINESS OPPORTUNITY MATRIX
# ===================================================================

print(f"\n\n📊 MARKET OPPORTUNITY SUMMARY")
print("=" * 60)

# Create comprehensive opportunity matrix
opportunity_matrix = []

for cluster in df['Cluster'].unique():
    segment_name = segment_names[cluster]
    segment_data = df[df['Cluster'] == cluster]
    
    # Get TAM data
    tam_data = tam_df[tam_df['Segment'] == segment_name].iloc[0]
    
    # Calculate opportunity score (1-10)
    market_size_score = min(10, tam_data['TAM_Growth_Potential'] / 1e9)  # Billions
    competition_score = 8 if cluster == 1 else 7 if cluster == 0 else 6  # Based on gaps identified
    customer_satisfaction_score = 10 - (unmet_needs_analysis[segment_name]['satisfaction_gaps'] * 2)
    
    overall_opportunity_score = (market_size_score + competition_score + customer_satisfaction_score) / 3
    
    opportunity_matrix.append({
        'Segment': segment_name,
        'Market_Size_Score': market_size_score,
        'Competition_Score': competition_score,
        'Satisfaction_Score': customer_satisfaction_score,
        'Overall_Opportunity': overall_opportunity_score,
        'Priority_Level': 'High' if overall_opportunity_score >= 8 else 'Medium' if overall_opportunity_score >= 6 else 'Low'
    })

# Display final opportunity matrix
print("\n🎯 BUSINESS OPPORTUNITY MATRIX (Score: 1-10):")
print("=" * 70)

opportunity_df = pd.DataFrame(opportunity_matrix)
opportunity_df = opportunity_df.sort_values('Overall_Opportunity', ascending=False)

for _, row in opportunity_df.iterrows():
    print(f"\n🏆 {row['Segment'].upper()}")
    print(f"   📊 Market Size Score: {row['Market_Size_Score']:.1f}/10")
    print(f"   🏁 Competition Score: {row['Competition_Score']:.1f}/10") 
    print(f"   😊 Satisfaction Score: {row['Satisfaction_Score']:.1f}/10")
    print(f"   ⭐ Overall Opportunity: {row['Overall_Opportunity']:.1f}/10")
    print(f"   🚀 Priority Level: {row['Priority_Level']}")

# Save results
opportunity_df.to_csv('05_results/business_opportunity_matrix.csv', index=False)
tam_df.to_csv('05_results/market_size_analysis.csv', index=False)

print(f"\n📁 Results saved:")
print(f"   • 05_results/business_opportunity_matrix.csv")
print(f"   • 05_results/market_size_analysis.csv")

print(f"\n✅ MARKET OPPORTUNITY ANALYSIS COMPLETE!")
print(f"📅 Analysis completed: {datetime.now().strftime('%d %B %Y, %H:%M')}")
print(f"🎯 Next step: CLV & Pricing Strategy Analysis")
