import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="BizVizion - Business Forecasting & AI Advisory",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'business_data' not in st.session_state:
    st.session_state.business_data = {}
if 'forecast_data' not in st.session_state:
    st.session_state.forecast_data = {}
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = 'normal'

# Enhanced Custom CSS for visual appeal
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.1;
    }
    
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.15);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        border: 1px solid rgba(0,0,0,0.05);
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    
    .ai-assistant-intro {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin: 2rem 0;
        position: relative;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        overflow: hidden;
    }
    
    .ai-assistant-intro::before {
        content: '🤖';
        position: absolute;
        top: -20px;
        right: -20px;
        font-size: 120px;
        opacity: 0.1;
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-20px) rotate(5deg); }
    }
    
    .scenario-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 500;
        margin: 0.25rem;
        transition: all 0.3s ease;
    }
    
    .scenario-normal {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
    }
    
    .scenario-growth {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
    }
    
    .scenario-recession {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
    }
    
    .glassmorphism {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .call-to-action {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    
    .demo-chart-container {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border: 1px solid rgba(102, 126, 234, 0.1);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    h1, h2, h3 {
        font-weight: 600;
        line-height: 1.2;
    }
    
    .stButton > button {
        border-radius: 12px;
        border: none;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

# Main Landing Page
def main_page():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🚀 BizVizion</h1>
        <h3>Your AI-Powered Business Companion</h3>
        <p>Project your future, manage payroll, and get growth ideas with AI and real-time data</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Assistant Introduction
    st.markdown("""
    <div class="ai-assistant-intro">
        <h2>👋 Meet Your AI Business Assistant</h2>
        <p>I'm here to help you understand where your business is heading and provide actionable insights for growth. Let's explore your business potential together!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Core Features Overview
    st.subheader("🎯 What BizVizion Can Do For You")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">📈</span>
            <h4>Business Forecasting</h4>
            <p>See where your business is heading in the next 5, 10, 15 years under best, worst, and expected conditions. Get detailed revenue, expense, and profit projections.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">💼</span>
            <h4>Payroll Cost Calculator</h4>
            <p>Understand comprehensive payroll costs including taxes, benefits, and employee efficiency metrics with detailed breakdowns.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🤖</span>
            <h4>AI Visible Assistant</h4>
            <p>Get smart, actionable growth ideas with an interactive AI that responds based on your business metrics and industry analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <span class="feature-icon">🎭</span>
            <h4>Scenario Simulation</h4>
            <p>Predict and simulate the impact of economic crashes, inflation spikes, aggressive competition, and market changes.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Demo Chart with Economic Scenarios
    st.markdown('<div class="demo-chart-container">', unsafe_allow_html=True)
    st.subheader("📊 Interactive Business Forecast Preview")
    
    # Scenario selector for demo
    col1, col2, col3 = st.columns(3)
    
    with col1:
        demo_scenario = st.selectbox(
            "Preview Economic Scenario:",
            ["normal", "growth", "recession"],
            index=0,
            format_func=lambda x: f"📈 Growth" if x == "growth" else f"📉 Recession" if x == "recession" else f"➡️ Normal"
        )
    
    with col2:
        demo_industry = st.selectbox(
            "Industry Example:",
            ["Technology", "Healthcare", "Retail", "Manufacturing", "Services"],
            index=0
        )
    
    with col3:
        demo_revenue = st.number_input(
            "Starting Revenue ($):",
            min_value=100000,
            max_value=10000000,
            value=500000,
            step=50000
        )
    
    # Create enhanced sample forecast data
    years = list(range(2025, 2041))
    
    # Scenario-based growth rates
    scenario_params = {
        'normal': {'growth': 0.08, 'volatility': 0.15},
        'growth': {'growth': 0.15, 'volatility': 0.12},
        'recession': {'growth': 0.02, 'volatility': 0.25}
    }
    
    # Industry multipliers
    industry_multipliers = {
        'Technology': 1.3,
        'Healthcare': 1.1,
        'Retail': 0.9,
        'Manufacturing': 1.0,
        'Services': 1.0
    }
    
    base_growth = scenario_params[demo_scenario]['growth'] * industry_multipliers.get(demo_industry, 1.0)
    
    best_case = [demo_revenue * ((1 + base_growth + 0.05) ** i) for i in range(len(years))]
    expected_case = [demo_revenue * ((1 + base_growth) ** i) for i in range(len(years))]
    worst_case = [demo_revenue * ((1 + max(0, base_growth - 0.08)) ** i) for i in range(len(years))]
    
    fig = go.Figure()
    
    # Add uncertainty band
    fig.add_trace(go.Scatter(
        x=years + years[::-1],
        y=best_case + worst_case[::-1],
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False,
        name='Projection Range'
    ))
    
    fig.add_trace(go.Scatter(
        x=years, 
        y=best_case, 
        mode='lines', 
        name='Best Case Scenario', 
        line=dict(color='#2ecc71', width=3, dash='dot')
    ))
    fig.add_trace(go.Scatter(
        x=years, 
        y=expected_case, 
        mode='lines+markers', 
        name='Expected Scenario', 
        line=dict(color='#667eea', width=4),
        marker=dict(size=6)
    ))
    fig.add_trace(go.Scatter(
        x=years, 
        y=worst_case, 
        mode='lines', 
        name='Worst Case Scenario', 
        line=dict(color='#e74c3c', width=3, dash='dot')
    ))
    
    fig.update_layout(
        title=f"15-Year Revenue Projection - {demo_industry} Industry ({demo_scenario.title()} Scenario)",
        xaxis_title="Year",
        yaxis_title="Revenue ($)",
        hovermode='x unified',
        template='plotly_white',
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Format y-axis as currency
    fig.update_layout(yaxis=dict(tickformat='$,.0f'))
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display scenario insights
    final_expected = expected_case[-1]
    growth_percentage = ((final_expected / demo_revenue) - 1) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("15-Year Growth", f"{growth_percentage:.0f}%")
    with col2:
        st.metric("Final Revenue", f"${final_expected:,.0f}")
    with col3:
        cagr = ((final_expected / demo_revenue) ** (1/15)) - 1
        st.metric("CAGR", f"{cagr:.1f}%")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Enhanced Call to Action
    st.markdown("""
    <div class="call-to-action">
        <h2>🚀 Ready to Transform Your Business?</h2>
        <p>Join thousands of small business owners who are already using BizVizion to make smarter decisions and accelerate their growth.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 Enter Business Data", type="primary", use_container_width=True):
            st.switch_page("pages/1_Business_Input.py")
        st.caption("Start by entering your business information")
    
    with col2:
        if st.button("📊 View Sample Dashboard", use_container_width=True):
            st.switch_page("pages/2_Forecasting_Dashboard.py")
        st.caption("Explore forecasting and analytics")
    
    with col3:
        if st.button("🤖 Ask Me Anything", use_container_width=True):
            st.switch_page("pages/3_AI_Assistant.py")
        st.caption("Chat with your AI business advisor")

# Sidebar Navigation
def sidebar():
    st.sidebar.title("🚀 BizVizion")
    st.sidebar.markdown("---")
    
    # Navigation
    st.sidebar.subheader("Navigation")
    
    if st.sidebar.button("🏠 Home", use_container_width=True):
        st.switch_page("app.py")
    
    if st.sidebar.button("📝 Business Input", use_container_width=True):
        st.switch_page("pages/1_Business_Input.py")
    
    if st.sidebar.button("📊 Forecasting Dashboard", use_container_width=True):
        st.switch_page("pages/2_Forecasting_Dashboard.py")
    
    if st.sidebar.button("🤖 AI Assistant", use_container_width=True):
        st.switch_page("pages/3_AI_Assistant.py")
    
    if st.sidebar.button("💼 Payroll Manager", use_container_width=True):
        st.switch_page("pages/4_Payroll_Manager.py")
    
    if st.sidebar.button("🗄️ Database Manager", use_container_width=True):
        st.switch_page("pages/5_Database_Manager.py")
    
    st.sidebar.markdown("---")
    
    # Enhanced Current Business Overview
    if st.session_state.business_data:
        st.sidebar.markdown("---")
        st.sidebar.subheader("📋 Current Business")
        data = st.session_state.business_data
        
        # Business info in cards
        if 'business_name' in data:
            st.sidebar.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1rem; border-radius: 8px; margin: 0.5rem 0; text-align: center;">
                <strong>{data['business_name']}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        if 'industry' in data:
            st.sidebar.markdown(f"**Industry:** {data['industry']}")
        if 'annual_revenue' in data:
            st.sidebar.markdown(f"**Revenue:** ${data['annual_revenue']:,}")
        if 'employees' in data:
            st.sidebar.markdown(f"**Employees:** {data['employees']}")
        
        # Quick metrics
        if 'annual_revenue' in data and 'annual_expenses' in data:
            profit = data['annual_revenue'] - data['annual_expenses']
            profit_margin = (profit / data['annual_revenue']) * 100 if data['annual_revenue'] > 0 else 0
            st.sidebar.markdown(f"**Profit Margin:** {profit_margin:.1f}%")
    
    # Enhanced Scenario Selector
    st.sidebar.markdown("---")
    st.sidebar.subheader("🎭 Economic Scenario")
    
    # Scenario badges
    scenario_options = ["normal", "growth", "recession"]
    scenario_emojis = {"normal": "➡️", "growth": "📈", "recession": "📉"}
    scenario_colors = {
        "normal": "#3498db", 
        "growth": "#2ecc71", 
        "recession": "#e74c3c"
    }
    
    for scenario_opt in scenario_options:
        is_active = scenario_opt == st.session_state.current_scenario
        color = scenario_colors[scenario_opt]
        opacity = "1.0" if is_active else "0.7"
        
        if st.sidebar.button(
            f"{scenario_emojis[scenario_opt]} {scenario_opt.title()}", 
            key=f"sidebar_{scenario_opt}",
            use_container_width=True
        ):
            st.session_state.current_scenario = scenario_opt
            st.rerun()
    
    # Display current scenario info
    scenario_descriptions = {
        'growth': "Economic expansion, increased consumer spending",
        'normal': "Stable economic conditions, typical growth",
        'recession': "Economic downturn, reduced spending"
    }
    
    current_desc = scenario_descriptions.get(st.session_state.current_scenario, "")
    st.sidebar.caption(f"Current: {current_desc}")

# Main execution
sidebar()
main_page()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>BizVizion - Empowering Small Businesses with AI-Driven Insights</p>
    <p>Built with ❤️ using Streamlit and OpenAI</p>
</div>
""", unsafe_allow_html=True)
