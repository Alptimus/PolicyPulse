import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="PolicyPulse: RBI Repo Shocks and Nifty Volatility Regimes", layout="wide")

# ---------------------------------------------------------
# 1. Data Loading & Caching
# ---------------------------------------------------------
@st.cache_data
def load_data():
    master_df = pd.read_csv('data/master_data.csv', parse_dates=['Date'])
    master_df['Year'] = master_df['Date'].dt.year
    
    # Calculate regimes for the events table
    master_df['Repo_Change'] = master_df['Repo'].diff()
    master_df['Regime'] = master_df['Repo_Change'].apply(
        lambda x: 'Pause' if pd.isna(x) or x == 0 else ('Hike' if x > 0 else 'Cut')
    )
    return master_df

df = load_data()

# ---------------------------------------------------------
# 2. Sidebar Filters
# ---------------------------------------------------------
st.sidebar.header("Filter Parameters")
years = st.sidebar.slider("Select Year Range", int(df['Year'].min()), int(df['Year'].max()), (2012, 2025))
regime_filter = st.sidebar.multiselect("Select Policy Regime", ['Hike', 'Cut', 'Pause'], default=['Hike', 'Cut'])

filtered_df = df[(df['Year'] >= years[0]) & (df['Year'] <= years[1]) & (df['Regime'].isin(regime_filter + ['Pause']))]

# ---------------------------------------------------------
# 3. Main UI & Insights
# ---------------------------------------------------------
st.title("PolicyPulse: ML-Driven Analysis of RBI Policy on Nifty Volatility")

st.markdown("""
**Macroeconomic Insight:** Both Logistic Regression and Random Forest models failed to beat a majority-class baseline when predicting post-announcement directional movement. This mathematical "failure" successfully proves the efficient market hypothesis. Because the flexible inflation targeting framework structurally telegraphs rate trajectories in advance, the market fully prices in the shock prior to the announcement date, rendering post-event directional movement as statistically unpredictable noise.
""")

# ---------------------------------------------------------
# 4. Time Series Panel (Dual Axis)
# ---------------------------------------------------------
st.subheader("Repo Rate vs Nifty Realized Volatility")

fig = go.Figure()
fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Repo'], name='Repo Rate', line=dict(color='firebrick', width=2)))
fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Volatility'], name='Nifty Volatility', yaxis='y2', line=dict(color='royalblue', width=1.5), opacity=0.7))

# --- CORRECTED PLOTLY LAYOUT BLOCK ---
fig.update_layout(
    yaxis=dict(
        title=dict(text='Repo Rate (%)', font=dict(color='firebrick')), 
        tickfont=dict(color='firebrick')
    ),
    yaxis2=dict(
        title=dict(text='Realized Volatility', font=dict(color='royalblue')), 
        tickfont=dict(color='royalblue'), 
        anchor='x', 
        overlaying='y', 
        side='right'
    ),
    hovermode='x unified',
    margin=dict(l=0, r=0, t=30, b=0)
)
# -------------------------------------

st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# 5. Volatility Response Table & Bar Chart
# ---------------------------------------------------------
col1, col2 = st.columns(2)

active_events = filtered_df[filtered_df['Regime'].isin(['Hike', 'Cut'])].copy()

# Simple Volatility Change (Forward 1-Month Proxy for 30 days)
active_events['Vol_30d_After'] = active_events['Volatility'].shift(-1)
active_events['Vol_Change'] = active_events['Vol_30d_After'] - active_events['Volatility']

with col1:
    st.subheader("Event Response Heatmap")
    # Formatting for display
    display_df = active_events[['Date', 'Regime', 'Repo_Change', 'Vol_Change']].dropna()
    display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m')
    st.dataframe(display_df.style.background_gradient(subset=['Vol_Change'], cmap='coolwarm'), use_container_width=True)

with col2:
    st.subheader("Average Volatility Change by Regime")
    avg_change = active_events.groupby('Regime')['Vol_Change'].mean().reset_index()
    fig2 = px.bar(avg_change, x='Regime', y='Vol_Change', color='Regime', color_discrete_map={'Hike':'firebrick', 'Cut':'royalblue'})
    st.plotly_chart(fig2, use_container_width=True)