import streamlit as st
from utils.page_config import set_page_config
from utils.i18n import get_translations
set_page_config("History")

import pandas as pd
import plotly.graph_objects as go
import json
import os
from components.sidebar import show_sidebar
from components.ai_chat import floating_chat
from datetime import datetime

t = get_translations()

# Hide default sidebar navigation
st.markdown('''
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
        .scope-header {
            color: #2e7d32;
            border-bottom: 2px solid #2e7d32;
            padding-bottom: 10px;
            margin: 20px 0;
        }
        .metric-card {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .metric-title {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 0.5rem;
        }
        .metric-value {
            color: #2e7d32;
            font-size: 1.5em;
            font-weight: 600;
        }
        .download-button {
            background-color: #2e7d32;
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 4px;
            text-decoration: none;
            display: inline-block;
            margin: 1rem 0;
            text-align: center;
            width: 100%;
            font-weight: bold;
            cursor: pointer;
        }
        .download-button:hover {
            background-color: #1b5e20;
        }
    </style>
''', unsafe_allow_html=True)

# Show custom sidebar
show_sidebar()

# Check authentication
if not st.session_state.get('authenticated', False):
    st.switch_page("Home.py")

st.title("📈 " + t.get("history", "History"))

try:
    # Get user's footprint history from json_storage
    from utils.json_storage import get_user_footprints
    
    # Get the current user's ID from session state
    user_id = st.session_state.get('user_id')
    if not user_id:
        st.error("User not authenticated")
        st.stop()
        
    # Get user's footprints
    footprints = get_user_footprints(user_id)
    
    # Sort by creation date, descending
    footprints = sorted(footprints, key=lambda x: x.get('created_at', 0), reverse=True)
    
    if not footprints:
        st.info("📃 " + t.get("no_history", "No calculation history yet. Try calculating your carbon footprint first!"))
        if st.button("🌍 " + t.get("go_to_calculator", "Go to Calculator")):
            st.switch_page("pages/2_Calculator.py")
        st.stop()
    
    # Get latest footprint
    latest = footprints[0]
    
    # Display latest emissions overview
    st.subheader("📈 " + t.get("latest_carbon_footprint_overview", "Latest Carbon Footprint Overview"))
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''<div class="metric-card"><div class="metric-title">🏭 {t.get('scope1_emissions', 'Scope 1 Emissions')}</div><div class="metric-value">{latest['scope1_emissions']:.1f} kgCO₂e</div></div>''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''<div class="metric-card"><div class="metric-title">⚡ {t.get('scope2_emissions', 'Scope 2 Emissions')}</div><div class="metric-value">{latest['scope2_emissions']:.1f} kgCO₂e</div></div>''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''<div class="metric-card"><div class="metric-title">🌐 {t.get('scope3_emissions', 'Scope 3 Emissions')}</div><div class="metric-value">{latest['scope3_emissions']:.1f} kgCO₂e</div></div>''', unsafe_allow_html=True)
    
    # Display total emissions
    st.markdown(f'''<div class="metric-card" style="margin-top: 1rem;"><div class="metric-title">🌍 {t.get('total_carbon_footprint', 'Total Carbon Footprint')}</div><div class="metric-value" style="font-size: 2em;">{latest['total_emissions']:.1f} kgCO₂e</div><div style="color: #666; font-size: 0.9em;">{latest['total_emissions']/1000:.2f} Metric Tons</div></div>''', unsafe_allow_html=True)
    
    # Add download report button
    if st.button("📄 " + t.get("download_report", "Download Detailed Report"), type="primary", use_container_width=True):
        try:
            from utils.pdf_generator import get_report_download_link
            from types import SimpleNamespace
            
            # Convert dictionary to object with attributes
            report_data = SimpleNamespace(**latest)
            
            # Get timestamp for filename
            timestamp = datetime.fromtimestamp(latest.get('created_at', datetime.now().timestamp()))
            pdf_data = get_report_download_link(report_data)
            
            st.download_button(
                label="📄 " + t.get("click_to_download_pdf", "Click to Download PDF Report"),
                data=pdf_data,
                file_name=f"carbon_footprint_report_{timestamp.strftime('%Y%m%d')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        except Exception as e:
            st.error("❌ " + t.get("report_generation_error", "Error generating report: ") + str(e))
    
    # Create emission breakdown charts
    st.subheader("📁 " + t.get("detailed_emission_breakdown", "Detailed Emission Breakdown"))
    
    # Prepare data for charts
    details = latest['emission_details']
    
    # Create three columns for scope breakdowns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🏭 " + t.get("scope1_breakdown", "Scope 1 Breakdown"))
        scope1_data = pd.DataFrame({
            'Category': list(details['scope1'].keys()),
            'Emissions': list(details['scope1'].values())
        })
        fig1 = go.Figure(data=[go.Pie(
            labels=scope1_data['Category'],
            values=scope1_data['Emissions'],
            hole=.3
        )])
        fig1.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig1, use_container_width=True)
        st.dataframe(
            scope1_data.style.format({'Emissions': '{:.1f}'}),
            hide_index=True,
            use_container_width=True
        )
    
    with col2:
        st.markdown("### ⚡ " + t.get("scope2_breakdown", "Scope 2 Breakdown"))
        scope2_data = pd.DataFrame({
            'Category': list(details['scope2'].keys()),
            'Emissions': list(details['scope2'].values())
        })
        fig2 = go.Figure(data=[go.Pie(
            labels=scope2_data['Category'],
            values=scope2_data['Emissions'],
            hole=.3
        )])
        fig2.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(
            scope2_data.style.format({'Emissions': '{:.1f}'}),
            hide_index=True,
            use_container_width=True
        )
    
    with col3:
        st.markdown("### 🌐 " + t.get("scope3_breakdown", "Scope 3 Breakdown"))
        scope3_data = pd.DataFrame({
            'Category': list(details['scope3'].keys()),
            'Emissions': list(details['scope3'].values())
        })
        fig3 = go.Figure(data=[go.Pie(
            labels=scope3_data['Category'],
            values=scope3_data['Emissions'],
            hole=.3
        )])
        fig3.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
        st.plotly_chart(fig3, use_container_width=True)
        st.dataframe(
            scope3_data.style.format({'Emissions': '{:.1f}'}),
            hide_index=True,
            use_container_width=True
        )
    
    # Historical Trends
    st.subheader("📈 " + t.get("historical_trends", "Historical Trends"))
    
    # Prepare historical data
    hist_data = pd.DataFrame([
        {
            'Date': pd.to_datetime(f['created_at'], unit='s'),
            'Scope 1': f['scope1_emissions'],
            'Scope 2': f['scope2_emissions'],
            'Scope 3': f['scope3_emissions'],
            'Total': f['total_emissions']
        } for f in footprints
    ])
    
    # Create line chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist_data['Date'], y=hist_data['Scope 1'], name=t.get('scope1', 'Scope 1'), line=dict(color='#2e7d32')))
    fig.add_trace(go.Scatter(x=hist_data['Date'], y=hist_data['Scope 2'], name=t.get('scope2', 'Scope 2'), line=dict(color='#1976d2')))
    fig.add_trace(go.Scatter(x=hist_data['Date'], y=hist_data['Scope 3'], name=t.get('scope3', 'Scope 3'), line=dict(color='#ff9800')))
    fig.add_trace(go.Scatter(x=hist_data['Date'], y=hist_data['Total'], name=t.get('total', 'Total'), line=dict(color='#d32f2f', dash='dash')))
    
    fig.update_layout(
        title=t.get('emissions_over_time', 'Emissions Over Time'),
        xaxis_title=t.get('date', 'Date'),
        yaxis_title=t.get('emissions_kgco2e', 'Emissions (kgCO₂e)'),
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table
    st.subheader("📋 " + t.get("detailed_history", "Detailed History"))
    st.dataframe(
        hist_data.style.format({
            'Scope 1': '{:.1f}',
            'Scope 2': '{:.1f}',
            'Scope 3': '{:.1f}',
            'Total': '{:.1f}'
        }),
        hide_index=True,
        use_container_width=True
    )

except Exception as e:
    st.error(t.get("error_loading_history", "Error loading history:") + f" {str(e)}")

# Add floating chat
floating_chat()
