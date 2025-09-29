#!/usr/bin/env python3
"""
🎨 FIGMA-STYLE PITCH DECK VISUAL GENERATOR
Creates professional pitch deck visuals with charts and mockups
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle
import seaborn as sns
from datetime import datetime, timedelta
import os

# Set the style for professional look
plt.style.use('dark_background')
sns.set_palette("husl")

def create_market_size_chart():
    """Create market size and growth chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor('#0a0a0a')
    
    # Market Growth Chart
    years = [2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032]
    market_size = [4.8, 6.0, 7.4, 9.1, 11.2, 13.8, 17.0, 21.0, 27.0]
    
    ax1.plot(years, market_size, marker='o', linewidth=4, markersize=10, color='#00ff88')
    ax1.fill_between(years, market_size, alpha=0.3, color='#00ff88')
    ax1.set_title('AI Code Tools Market Growth\n$4.8B → $27B (23% CAGR)', 
                  fontsize=20, color='white', fontweight='bold')
    ax1.set_xlabel('Year', fontsize=14, color='white')
    ax1.set_ylabel('Market Size ($B)', fontsize=14, color='white')
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(colors='white', labelsize=12)
    
    # Market Segments Pie Chart
    segments = ['Fintech\n30%', 'Gaming\n25%', 'Security\n20%', 'Enterprise\n25%']
    sizes = [30, 25, 20, 25]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4']
    
    ax2.pie(sizes, labels=segments, colors=colors, autopct='', 
            startangle=90, textprops={'fontsize': 14, 'color': 'white'})
    ax2.set_title('Code Validation Market\nSegments ($2.1B TAM)', 
                  fontsize=20, color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('market_opportunity.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    print("✅ Market opportunity chart saved as market_opportunity.png")

def create_competitive_comparison():
    """Create competitive comparison table"""
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('#0a0a0a')
    
    # Data for comparison
    features = ['Multi-Agent\nConsensus', 'Content\nNeutral', 'Self-Improving\nAI', 
                'Quantum\nSecurity', 'Real-time\nValidation']
    companies = ['DeepSeek\nSuite', 'Guardrails.ai', 'GitHub\nCopilot', 'SonarQube']
    
    data = [
        [1, 0, 0, 0],  # Multi-Agent
        [1, 0.5, 0, 0.5],  # Content Neutral
        [1, 0, 0.5, 0],  # Self-Improving
        [1, 0, 0, 0],  # Quantum Security
        [1, 0, 1, 0.5]  # Real-time
    ]
    
    # Create heatmap
    im = ax.imshow(data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    # Set ticks and labels
    ax.set_xticks(np.arange(len(companies)))
    ax.set_yticks(np.arange(len(features)))
    ax.set_xticklabels(companies, fontsize=14, color='white')
    ax.set_yticklabels(features, fontsize=14, color='white')
    
    # Add text annotations
    for i in range(len(features)):
        for j in range(len(companies)):
            if data[i][j] == 1:
                text = "✅"
            elif data[i][j] == 0.5:
                text = "⚠️"
            else:
                text = "❌"
            ax.text(j, i, text, ha="center", va="center", 
                   color="white", fontsize=20)
    
    ax.set_title('Competitive Analysis Matrix\nDeepSeek Suite vs Competitors', 
                fontsize=24, color='white', fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('competitive_analysis.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    print("✅ Competitive analysis chart saved as competitive_analysis.png")

def create_revenue_projections():
    """Create revenue projection charts"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.patch.set_facecolor('#0a0a0a')
    
    # Revenue Growth Chart
    years = ['2025', '2026', '2027']
    revenue = [1.2, 4.8, 12.6]
    users = [15000, 45000, 120000]
    
    ax1.bar(years, revenue, color=['#ff6b6b', '#4ecdc4', '#45b7d1'], alpha=0.8)
    ax1.set_title('Revenue Projections\n163-300% YoY Growth', 
                  fontsize=18, color='white', fontweight='bold')
    ax1.set_ylabel('Revenue ($M)', fontsize=14, color='white')
    ax1.tick_params(colors='white', labelsize=12)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for i, v in enumerate(revenue):
        ax1.text(i, v + 0.2, f'${v}M', ha='center', va='bottom', 
                color='white', fontsize=14, fontweight='bold')
    
    # User Growth Chart
    ax2.plot(years, users, marker='o', linewidth=4, markersize=12, color='#00ff88')
    ax2.fill_between(years, users, alpha=0.3, color='#00ff88')
    ax2.set_title('User Base Growth\n15K → 120K Users', 
                  fontsize=18, color='white', fontweight='bold')
    ax2.set_ylabel('Active Users', fontsize=14, color='white')
    ax2.tick_params(colors='white', labelsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Unit Economics
    metrics = ['CAC', 'LTV', 'Gross\nMargin']
    values = [45, 1847, 85]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    bars = ax3.bar(metrics, values, color=colors, alpha=0.8)
    ax3.set_title('Unit Economics\nLTV/CAC = 41x', 
                  fontsize=18, color='white', fontweight='bold')
    ax3.tick_params(colors='white', labelsize=12)
    ax3.grid(True, alpha=0.3)
    
    # Add value labels
    labels = ['$45', '$1,847', '85%']
    for i, (bar, label) in enumerate(zip(bars, labels)):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 20,
                label, ha='center', va='bottom', color='white', 
                fontsize=14, fontweight='bold')
    
    # Funding Use Pie Chart
    use_of_funds = ['Engineering\n60%', 'Sales/Marketing\n25%', 'Operations\n15%']
    funding_amounts = [60, 25, 15]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    ax4.pie(funding_amounts, labels=use_of_funds, colors=colors, autopct='$%.1fM',
            startangle=90, textprops={'fontsize': 12, 'color': 'white'})
    ax4.set_title('$2M Seed Funding\nUse of Funds', 
                  fontsize=18, color='white', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('revenue_projections.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    print("✅ Revenue projections chart saved as revenue_projections.png")

def create_traction_metrics():
    """Create traction and user metrics dashboard"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    fig.patch.set_facecolor('#0a0a0a')
    
    # User Retention Curve
    weeks = np.arange(1, 13)
    retention = [100, 85, 78, 72, 68, 65, 63, 61, 60, 59, 58, 57]
    
    ax1.plot(weeks, retention, marker='o', linewidth=4, markersize=10, color='#00ff88')
    ax1.fill_between(weeks, retention, alpha=0.3, color='#00ff88')
    ax1.set_title('Weekly User Retention\n85% Week 1 Retention', 
                  fontsize=18, color='white', fontweight='bold')
    ax1.set_xlabel('Weeks', fontsize=14, color='white')
    ax1.set_ylabel('Retention (%)', fontsize=14, color='white')
    ax1.tick_params(colors='white', labelsize=12)
    ax1.grid(True, alpha=0.3)
    
    # NPS Score
    ax2.bar(['Detractors', 'Passives', 'Promoters'], [8, 15, 77], 
            color=['#ff6b6b', '#ffa726', '#4ecdc4'], alpha=0.8)
    ax2.set_title('Net Promoter Score\n4.7/5.0 Rating', 
                  fontsize=18, color='white', fontweight='bold')
    ax2.set_ylabel('Percentage (%)', fontsize=14, color='white')
    ax2.tick_params(colors='white', labelsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Usage Distribution by Category
    categories = ['Crypto', 'Gaming', 'Security', 'Fintech', 'Other']
    usage = [31, 24, 19, 16, 10]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#ffa726']
    
    ax3.pie(usage, labels=categories, colors=colors, autopct='%1.0f%%',
            startangle=90, textprops={'fontsize': 12, 'color': 'white'})
    ax3.set_title('Usage by Code Category\nCrypto Leading at 31%', 
                  fontsize=18, color='white', fontweight='bold')
    
    # Monthly Recurring Revenue Growth
    months = ['Month 1', 'Month 2', 'Month 3']
    mrr = [1200, 4500, 8400]
    
    bars = ax4.bar(months, mrr, color=['#ff6b6b', '#4ecdc4', '#45b7d1'], alpha=0.8)
    ax4.set_title('MRR Growth\n$8.4K Current MRR', 
                  fontsize=18, color='white', fontweight='bold')
    ax4.set_ylabel('MRR ($)', fontsize=14, color='white')
    ax4.tick_params(colors='white', labelsize=12)
    ax4.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, mrr):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 100,
                f'${value:,}', ha='center', va='bottom', color='white', 
                fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('traction_metrics.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    print("✅ Traction metrics dashboard saved as traction_metrics.png")

def create_go_to_market_timeline():
    """Create Go-to-Market timeline visualization"""
    fig, ax = plt.subplots(figsize=(20, 10))
    fig.patch.set_facecolor('#0a0a0a')
    
    # Timeline data
    phases = ['Phase 1\nDeveloper Community\n(Months 1-6)', 
              'Phase 2\nEnterprise Sales\n(Months 7-18)', 
              'Phase 3\nPlatform Ecosystem\n(Months 19+)']
    
    targets = ['10K free users\n500 paid conversions', 
               '50 enterprise customers\n$2M+ ARR',
               '$10M+ ARR\nNetwork effects']
    
    # Create timeline
    y_positions = [2, 1, 0]
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    
    for i, (phase, target, color) in enumerate(zip(phases, targets, colors)):
        # Phase box
        rect = Rectangle((i*6, y_positions[i]-0.3), 5, 0.6, 
                        facecolor=color, alpha=0.8, edgecolor='white')
        ax.add_patch(rect)
        
        # Phase text
        ax.text(i*6 + 2.5, y_positions[i], phase, ha='center', va='center',
                fontsize=14, color='white', fontweight='bold')
        
        # Target text
        ax.text(i*6 + 2.5, y_positions[i]-0.8, target, ha='center', va='center',
                fontsize=12, color='white')
        
        # Arrow
        if i < len(phases) - 1:
            ax.arrow(i*6 + 5.2, y_positions[i], 0.6, 0, 
                    head_width=0.1, head_length=0.2, fc='white', ec='white')
    
    ax.set_xlim(-1, 19)
    ax.set_ylim(-1.5, 3)
    ax.set_title('Go-to-Market Strategy Timeline\nPhased Approach to $10M+ ARR', 
                fontsize=24, color='white', fontweight='bold', pad=30)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig('gtm_timeline.png', dpi=300, bbox_inches='tight', 
                facecolor='#0a0a0a', edgecolor='none')
    print("✅ Go-to-Market timeline saved as gtm_timeline.png")

def create_all_visuals():
    """Generate all pitch deck visuals"""
    print("🎨 CREATING PITCH DECK VISUALS...")
    print("=" * 50)
    
    try:
        create_market_size_chart()
        create_competitive_comparison()
        create_revenue_projections()
        create_traction_metrics()
        create_go_to_market_timeline()
        
        print("\n🎉 ALL VISUALS CREATED SUCCESSFULLY!")
        print("📁 Files saved in current directory:")
        print("   • market_opportunity.png")
        print("   • competitive_analysis.png")
        print("   • revenue_projections.png")
        print("   • traction_metrics.png")
        print("   • gtm_timeline.png")
        
        print(f"\n💡 NEXT STEPS:")
        print("1. Import these visuals into Figma or PowerPoint")
        print("2. Add your branding and company logo")
        print("3. Create slide templates with dark theme")
        print("4. Practice your 10-minute pitch")
        print("5. Send to investors and close that $2M!")
        
    except Exception as e:
        print(f"❌ Error creating visuals: {e}")
        print("Make sure matplotlib, seaborn, numpy, and pandas are installed:")
        print("pip install matplotlib seaborn numpy pandas")

if __name__ == "__main__":
    print("🚀 DEEPSEEK AI VALIDATION SUITE - PITCH DECK VISUAL GENERATOR")
    print("Creating professional investor-grade charts and mockups...")
    print("=" * 70)
    
    create_all_visuals()
    
    print(f"\n🎯 YOUR PITCH DECK IS NOW INVESTOR-READY!")
    print("Time to raise that $2M seed round and dominate the $27B market! 🚀💰")