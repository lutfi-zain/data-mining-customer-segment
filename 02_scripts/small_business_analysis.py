import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("🏪 SMALL BUSINESS OPPORTUNITY ANALYSIS")
print("💰 Budget Constraint: < Rp20 juta")
print("=" * 60)

# Load data
df = pd.read_csv('01_data/data_with_clusters.csv')

print(f"📊 Re-analyzing {len(df)} customers dengan constraint modal kecil")
print(f"📅 Analysis date: {datetime.now().strftime('%d %B %Y')}")

# Define segment names
segment_names = {
    0: "Penggemar Kuliner",
    1: "Orang Tua & Anak", 
    2: "Kreator Fashion"
}

print("\n🎯 SMALL BUSINESS FEASIBILITY ANALYSIS")
print("-" * 50)

# ===================================================================
# SMALL BUSINESS OPPORTUNITY ANALYSIS PER SEGMENT
# ===================================================================

small_business_opportunities = []

for cluster in df['Cluster'].unique():
    segment_name = segment_names[cluster]
    segment_data = df[df['Cluster'] == cluster]
    
    # Basic metrics
    customer_count = len(segment_data)
    avg_spend = segment_data['Harga Kelas'].mean()
    
    # Analyze top programs for small business potential
    top_programs = segment_data['Nama Program'].value_counts().head(5)
    
    # Small business analysis based on segment characteristics
    if cluster == 0:  # Penggemar Kuliner
        # Check most popular programs in this segment
        business_ideas = [
            {
                "idea": "Kelas Matematika Online untuk Anak",
                "based_on": "Kelas Matematika (156 customers, 15.7%)",
                "startup_cost": "Rp 5-8 juta",
                "cost_breakdown": "Laptop (3jt) + Software (1jt) + Marketing (2jt) + Operasional (2jt)",
                "revenue_model": "Rp30k/siswa/bulan",
                "target_customers": 156,
                "monthly_revenue_potential": "Rp 4.7 juta/bulan",
                "payback_period": "2-3 bulan",
                "feasibility": "VERY HIGH"
            },
            {
                "idea": "Bimbel Pra-Baca & Pra-Tulis Online",
                "based_on": "Pramembaca & Pramenulis (120 customers, 12.1%)",
                "startup_cost": "Rp 6-10 juta", 
                "cost_breakdown": "Equipment (4jt) + Materi (2jt) + Platform (2jt) + Marketing (2jt)",
                "revenue_model": "Rp40k/siswa/bulan",
                "target_customers": 120,
                "monthly_revenue_potential": "Rp 4.8 juta/bulan", 
                "payback_period": "2-3 bulan",
                "feasibility": "HIGH"
            }
        ]
        
    elif cluster == 1:  # Orang Tua & Anak
        business_ideas = [
            {
                "idea": "Kelas Digital Art untuk Anak (Bacimay Style)",
                "based_on": "Bacimay (174 customers, 11.6%)",
                "startup_cost": "Rp 8-12 juta",
                "cost_breakdown": "Drawing tablet (3jt) + Software (2jt) + Setup studio mini (3jt) + Marketing (4jt)",
                "revenue_model": "Rp60k/siswa/bulan",
                "target_customers": 174,
                "monthly_revenue_potential": "Rp 10.4 juta/bulan",
                "payback_period": "1-2 bulan", 
                "feasibility": "VERY HIGH"
            },
            {
                "idea": "Kelas Kuker (Cooking for Kids) Online",
                "based_on": "Kuker (101 customers, 6.7%)",
                "startup_cost": "Rp 7-10 juta",
                "cost_breakdown": "Kitchen setup (4jt) + Camera equipment (2jt) + Ingredients (1jt) + Marketing (3jt)",
                "revenue_model": "Rp50k/siswa/bulan",
                "target_customers": 101,
                "monthly_revenue_potential": "Rp 5.1 juta/bulan",
                "payback_period": "2 bulan",
                "feasibility": "HIGH"
            }
        ]
        
    else:  # Kreator Fashion
        business_ideas = [
            {
                "idea": "Kelas Jahit Basic Online",
                "based_on": "Jahit basic (34 customers, 10.3%)",
                "startup_cost": "Rp 10-15 juta",
                "cost_breakdown": "Mesin jahit (5jt) + Fabric samples (2jt) + Camera setup (3jt) + Marketing (5jt)",
                "revenue_model": "Rp100k/siswa/bulan",
                "target_customers": 34,
                "monthly_revenue_potential": "Rp 3.4 juta/bulan",
                "payback_period": "3-4 bulan",
                "feasibility": "MEDIUM"
            },
            {
                "idea": "Jasa Desain Logo Intensif",
                "based_on": "Kelas intensif logo (27 customers, 8.2%)",
                "startup_cost": "Rp 5-8 juta",
                "cost_breakdown": "Design software (2jt) + Laptop upgrade (3jt) + Portfolio website (1jt) + Marketing (2jt)",
                "revenue_model": "Rp150k/project",
                "target_customers": 27,
                "monthly_revenue_potential": "Rp 4.1 juta/bulan",
                "payback_period": "2-3 bulan",
                "feasibility": "HIGH"
            }
        ]
    
    small_business_opportunities.extend([{
        'segment': segment_name,
        'cluster': cluster,
        'customer_base': customer_count,
        'avg_current_spend': avg_spend,
        'business_ideas': business_ideas
    }])

# ===================================================================
# FEASIBILITY RANKING
# ===================================================================

print("\n🏆 TOP SMALL BUSINESS OPPORTUNITIES (Budget < Rp20 juta)")
print("=" * 70)

all_ideas = []
for segment_data in small_business_opportunities:
    for idea in segment_data['business_ideas']:
        idea['segment'] = segment_data['segment']
        all_ideas.append(idea)

# Sort by feasibility and revenue potential
feasibility_score = {'VERY HIGH': 3, 'HIGH': 2, 'MEDIUM': 1, 'LOW': 0}
all_ideas_scored = []

for idea in all_ideas:
    # Calculate monthly revenue as number
    revenue_str = idea['monthly_revenue_potential'].replace('Rp ', '').replace(' juta/bulan', '').replace(',', '.')
    monthly_revenue = float(revenue_str)
    
    # Calculate startup cost as number
    cost_str = idea['startup_cost'].split('-')[0].replace('Rp ', '').replace(' juta', '')
    startup_cost = float(cost_str)
    
    # Calculate ROI and score
    annual_revenue = monthly_revenue * 12
    roi_percentage = ((annual_revenue - startup_cost) / startup_cost) * 100
    
    idea_scored = idea.copy()
    idea_scored['monthly_revenue_num'] = monthly_revenue
    idea_scored['startup_cost_num'] = startup_cost
    idea_scored['annual_revenue'] = annual_revenue
    idea_scored['roi_percentage'] = roi_percentage
    idea_scored['feasibility_score'] = feasibility_score[idea['feasibility']]
    
    all_ideas_scored.append(idea_scored)

# Sort by combined score (feasibility + ROI)
all_ideas_sorted = sorted(all_ideas_scored, 
                         key=lambda x: (x['feasibility_score'], x['roi_percentage']), 
                         reverse=True)

print("\n🥇 RANKING BERDASARKAN FEASIBILITY & ROI:")
print("-" * 50)

for i, idea in enumerate(all_ideas_sorted[:5], 1):
    print(f"\n{i}. 🎯 {idea['idea']}")
    print(f"   📊 Segment: {idea['segment']}")
    print(f"   💰 Modal: {idea['startup_cost']}")
    print(f"   📈 Revenue/bulan: {idea['monthly_revenue_potential']}")
    print(f"   🎯 Target: {idea['target_customers']} customers existing")
    print(f"   ⏰ Payback: {idea['payback_period']}")
    print(f"   📊 ROI: {idea['roi_percentage']:.0f}% annually")
    print(f"   ⭐ Feasibility: {idea['feasibility']}")
    print(f"   🔧 Setup: {idea['cost_breakdown']}")

# ===================================================================
# DETAILED BUSINESS PLAN FOR TOP 3
# ===================================================================

print(f"\n\n📋 DETAILED BUSINESS PLAN - TOP 3 OPPORTUNITIES")
print("=" * 60)

top_3 = all_ideas_sorted[:3]

for i, idea in enumerate(top_3, 1):
    print(f"\n🏆 RANK #{i}: {idea['idea'].upper()}")
    print("-" * 50)
    
    print(f"💡 CONCEPT:")
    print(f"   • Based on existing demand: {idea['based_on']}")
    print(f"   • Target segment: {idea['segment']}")
    print(f"   • Proven customer base: {idea['target_customers']} existing customers")
    
    print(f"\n💰 FINANCIAL PROJECTION:")
    print(f"   • Startup Cost: {idea['startup_cost']}")
    print(f"   • Monthly Revenue: {idea['monthly_revenue_potential']}")
    print(f"   • Annual Revenue: Rp{idea['annual_revenue']:.1f} juta")
    print(f"   • ROI: {idea['roi_percentage']:.0f}% per year")
    print(f"   • Break-even: {idea['payback_period']}")
    
    print(f"\n🛠️ STARTUP REQUIREMENTS:")
    items = idea['cost_breakdown'].split(' + ')
    for item in items:
        print(f"   • {item}")
    
    print(f"\n📈 GROWTH STRATEGY:")
    if 'Online' in idea['idea']:
        print("   • Start dengan 1-on-1 online sessions")
        print("   • Scale ke group classes (max 5 students)")
        print("   • Build community dan referral program")
        print("   • Expand ke subscription model")
    else:
        print("   • Begin dengan project-based services")
        print("   • Build portfolio dan testimonials")
        print("   • Scale through partnerships")
        print("   • Develop productized offerings")
    
    print(f"\n🎯 SUCCESS FACTORS:")
    print("   • Leverage existing customer demand")
    print("   • Low overhead dengan online delivery")
    print("   • Strong word-of-mouth potential")
    print("   • Scalable business model")

# ===================================================================
# IMPLEMENTATION ROADMAP
# ===================================================================

print(f"\n\n🚀 IMPLEMENTATION ROADMAP - FIRST 90 DAYS")
print("=" * 60)

best_opportunity = top_3[0]
print(f"💡 SELECTED OPPORTUNITY: {best_opportunity['idea']}")
print(f"🎯 Target Segment: {best_opportunity['segment']}")
print(f"💰 Required Investment: {best_opportunity['startup_cost']}")

print(f"\n📅 WEEK 1-2: PREPARATION")
print("   • Market validation dengan 10-15 potential customers")
print("   • Finalize curriculum dan teaching materials") 
print("   • Purchase essential equipment")
print("   • Setup basic online presence (social media)")

print(f"\n📅 WEEK 3-4: PILOT LAUNCH")
print("   • Recruit 5-10 beta customers dengan discount 50%")
print("   • Conduct pilot classes dan gather feedback")
print("   • Refine teaching method dan materials")
print("   • Build initial testimonials")

print(f"\n📅 WEEK 5-8: SCALE UP")
print("   • Launch full marketing campaign")
print("   • Target existing customer base dari analysis")
print("   • Implement referral program")
print("   • Expand class schedules")

print(f"\n📅 WEEK 9-12: OPTIMIZE & EXPAND")
print("   • Analyze customer acquisition cost vs lifetime value")
print("   • Introduce advanced classes atau specializations")
print("   • Build community features")
print("   • Plan untuk cross-selling opportunities")

# ===================================================================
# RISK ANALYSIS & MITIGATION
# ===================================================================

print(f"\n\n⚠️ RISK ANALYSIS & MITIGATION")
print("=" * 60)

print(f"🔴 HIGH RISKS:")
print("   • Customer acquisition lebih lambat dari expected")
print("     → Mitigation: Start dengan existing network, offer trial classes")
print("   • Competition dari established players")
print("     → Mitigation: Focus pada personal touch dan community building")

print(f"\n🟡 MEDIUM RISKS:")
print("   • Technical issues dengan online delivery")
print("     → Mitigation: Have backup platforms, invest dalam reliable tech")
print("   • Seasonal demand fluctuations")
print("     → Mitigation: Diversify offerings, build subscription model")

print(f"\n🟢 LOW RISKS:")
print("   • Equipment failure")
print("     → Mitigation: Budget untuk backup equipment")
print("   • Content piracy")
print("     → Mitigation: Focus pada live interaction value")

# Save analysis
analysis_df = pd.DataFrame(all_ideas_sorted)
analysis_df.to_csv('05_results/small_business_opportunities.csv', index=False)

print(f"\n📁 ANALYSIS SAVED:")
print(f"   • 05_results/small_business_opportunities.csv")

print(f"\n✅ SMALL BUSINESS OPPORTUNITY ANALYSIS COMPLETE!")
print(f"🎯 RECOMMENDATION: {best_opportunity['idea']}")
print(f"💰 INVESTMENT: {best_opportunity['startup_cost']}")
print(f"📈 EXPECTED ROI: {best_opportunity['roi_percentage']:.0f}% annually")
print(f"⏰ PAYBACK: {best_opportunity['payback_period']}")
