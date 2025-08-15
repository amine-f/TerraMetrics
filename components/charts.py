import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def create_donut_chart(data, title="Emission Distribution"):
    """Create a donut chart for emission distribution."""
    fig = go.Figure(data=[go.Pie(
        labels=['Transportation', 'Electricity', 'Diet', 'Waste'],
        values=[data['Transportation'], data['Electricity'], 
                data['Diet'], data['Waste']],
        hole=.3,
        marker=dict(colors=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'])
    )])
    fig.update_layout(
        title=title,
        showlegend=True,
        height=400
    )
    return fig

def create_bar_chart(data):
    """Create a bar chart for emissions by category."""
    categories = ['Transportation', 'Electricity', 'Diet', 'Waste']
    values = [data['Transportation'], data['Electricity'], 
             data['Diet'], data['Waste']]
    
    fig = go.Figure(data=[go.Bar(
        x=categories,
        y=values,
        marker_color=['#FF9999', '#66B2FF', '#99FF99', '#FFCC99'],
        text=[f'{v:.2f}' for v in values],
        textposition='auto',
    )])
    fig.update_layout(
        title="Emissions by Category",
        yaxis_title="Tonnes CO2 per year",
        height=400,
        showlegend=False,
        bargap=0.2
    )
    return fig

def create_line_chart(df):
    """Create a line chart for historical trends."""
    df_melted = df.melt(
        id_vars=['Date'], 
        value_vars=['Transportation', 'Electricity', 'Diet', 'Waste'],
        var_name='Category', 
        value_name='Emissions'
    )
    
    fig = px.line(
        df_melted, 
        x='Date', 
        y='Emissions', 
        color='Category',
        title='Emissions Over Time'
    )
    fig.update_layout(height=400)
    return fig

def show_percentage_contribution(data):
    """Display percentage contribution of each category."""
    categories = ['Transportation', 'Electricity', 'Diet', 'Waste']
    values = [data['Transportation'], data['Electricity'], 
             data['Diet'], data['Waste']]
    total = sum(values)
    
    st.markdown("### Percentage Contribution")
    for cat, val in zip(categories, values):
        percentage = (val / total) * 100
        st.text(f"{cat}: {percentage:.1f}%")
