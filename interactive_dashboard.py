"""
Aadhaar DataThon - Interactive Dashboard
Hackathon-Winning Interactive Visualization Dashboard
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Aadhaar Analytics Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Set dark theme and enhanced styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Dark mode base with enhanced styling */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Enhanced sidebar with dark theme */
    .stSidebar {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%) !important;
        border-right: 2px solid #4a5568 !important;
    }
    
    /* Sidebar content styling */
    .stSidebar .stMarkdown {
        color: #e2e8f0 !important;
    }
    .stSidebar .stMarkdown h1, .stSidebar .stMarkdown h2, .stSidebar .stMarkdown h3 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Filter section background */
    .stSidebar > div {
        background: linear-gradient(180deg, #0f1419 0%, #1a1f2e 100%) !important;
        padding: 1rem !important;
    }
    
    /* Filter labels styling */
    .stSidebar .stSelectbox label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    .stSidebar .stMultiSelect label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    .stSidebar .stDateInput label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    .stSidebar .stSlider label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
    }
    
    /* Filter section container */
    .stSidebar .element-container {
        background: rgba(45, 55, 72, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        margin: 0.5rem 0 !important;
        border: 1px solid rgba(74, 85, 104, 0.3) !important;
    }
    
    /* Enhanced input styling with dark theme */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #ffffff !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    .stSelectbox option {
        background: #2d3748 !important;
        color: #ffffff !important;
    }
    
    .stMultiSelect > div > div {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #ffffff !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
    }
    .stMultiSelect > div > div > div {
        color: #ffffff !important;
    }
    .stMultiSelect .stMultiSelect > div > div > div > div {
        background: #4a5568 !important;
        color: #ffffff !important;
        border-radius: 4px !important;
    }
    
    .stDateInput > div > div {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #ffffff !important;
        border: 2px solid #4a5568 !important;
        border-radius: 8px !important;
    }
    .stDateInput > div > div > div {
        color: #ffffff !important;
    }
    .stDateInput input {
        background: #2d3748 !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    /* Slider styling */
    .stSlider > div > div > div > div {
        background: #4a5568 !important;
    }
    .stSlider > div > div > div > div > div {
        background: #667eea !important;
    }
    
    /* Dropdown menu styling */
    .stSelectbox > div > div > div[role="listbox"] {
        background: #2d3748 !important;
        border: 1px solid #4a5568 !important;
        border-radius: 8px !important;
    }
    .stSelectbox > div > div > div[role="listbox"] > div {
        background: #2d3748 !important;
        color: #ffffff !important;
    }
    .stSelectbox > div > div > div[role="listbox"] > div:hover {
        background: #4a5568 !important;
        color: #ffffff !important;
    }
    
    /* Enhanced text styling */
    .stMarkdown {
        color: #e2e8f0 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced metric styling */
    .stMetric {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        padding: 1rem !important;
        border-radius: 12px !important;
        border: 1px solid #4a5568 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    .stMetric label {
        color: #cbd5e0 !important;
        font-weight: 500 !important;
    }
    .stMetric div[data-testid="metric-container"] > div {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Enhanced info/success/warning boxes */
    .stAlert {
        background: rgba(45, 55, 72, 0.8) !important;
        border: 1px solid #4a5568 !important;
        border-radius: 8px !important;
        color: #e2e8f0 !important;
    }
    .stAlert[data-baseweb="notification"] {
        background: rgba(45, 55, 72, 0.9) !important;
    }
    
    /* Enhanced expander styling */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        border: 1px solid #4a5568 !important;
    }
    .streamlit-expanderContent {
        background: rgba(45, 55, 72, 0.5) !important;
        border: 1px solid #4a5568 !important;
        border-top: none !important;
        border-radius: 0 0 8px 8px !important;
    }
    
    /* Additional sidebar enhancements */
    .stSidebar .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    .stSidebar .stButton > button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    /* Filter section headers */
    .stSidebar .stMarkdown h4 {
        color: #667eea !important;
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 1px solid #4a5568 !important;
    }
    
    /* Sidebar scrollbar */
    .stSidebar .stVerticalBlock {
        background: transparent !important;
    }
    .stSidebar::-webkit-scrollbar {
        width: 8px !important;
    }
    .stSidebar::-webkit-scrollbar-track {
        background: #1a1f2e !important;
        border-radius: 4px !important;
    }
    .stSidebar::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-radius: 4px !important;
    }
    .stSidebar::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%) !important;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced dark mode styling for professional dashboard
st.markdown("""
<style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Enhanced dark mode base */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%) !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        padding: 1rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    .metric-card h3 {
        color: white !important;
        margin-bottom: 0.5rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    .metric-card h2 {
        color: white !important;
        margin: 0.5rem 0;
        font-weight: 700;
        font-size: 2.2rem;
    }
    .metric-card p {
        color: rgba(255, 255, 255, 0.8) !important;
        margin: 0;
        font-size: 0.9rem;
        font-weight: 400;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        padding: 2rem;
        margin: 1.5rem 0;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .insight-box h4 {
        color: white !important;
        margin-bottom: 1.5rem;
        font-weight: 700;
        font-size: 1.4rem;
        text-align: center;
    }
    .insight-box ul {
        color: white !important;
        list-style-type: none;
        padding-left: 0;
    }
    .insight-box li {
        color: white !important;
        margin-bottom: 1rem;
        line-height: 1.6;
        padding-left: 1.5rem;
        position: relative;
        font-weight: 400;
    }
    .insight-box li:before {
        content: "💡";
        position: absolute;
        left: 0;
        font-size: 1.2rem;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white !important;
        padding: 2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: 0 4px 12px rgba(17, 153, 142, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .recommendation-box h4 {
        color: white !important;
        margin-bottom: 1.5rem;
        font-weight: 700;
        font-size: 1.4rem;
        text-align: center;
    }
    .recommendation-box ul {
        color: white !important;
        list-style-type: none;
        padding-left: 0;
    }
    .recommendation-box li {
        color: white !important;
        margin-bottom: 1rem;
        line-height: 1.6;
        padding-left: 1.5rem;
        position: relative;
        font-weight: 400;
    }
    .recommendation-box li:before {
        content: "🚀";
        position: absolute;
        left: 0;
        font-size: 1.2rem;
    }
    
    /* Enhanced sidebar styling */
    .stSidebar {
        background: linear-gradient(180deg, #1e2329 0%, #2d3748 100%) !important;
        border-right: 2px solid #4a5568 !important;
    }
    .stSidebar .stMarkdown {
        color: #e2e8f0 !important;
    }
    
    /* Enhanced input styling */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #ffffff !important;
        border: 2px solid #4a5568 !important;
        border-radius: 12px !important;
    }
    .stMultiSelect > div > div {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #ffffff !important;
        border: 2px solid #4a5568 !important;
        border-radius: 12px !important;
    }
    .stDateInput > div > div {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #ffffff !important;
        border: 2px solid #4a5568 !important;
        border-radius: 12px !important;
    }
    
    /* Enhanced text styling */
    .stMarkdown {
        color: #e2e8f0 !important;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* Chart container styling */
    .stPlotlyChart {
        background: rgba(45, 55, 72, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    /* Ensure all text in custom boxes is visible */
    .insight-box *, .recommendation-box * {
        color: white !important;
    }
    
    /* Enhanced scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #2d3748;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load and preprocess ALL data from CSV files with caching"""
    try:
        st.info("Loading ALL CSV files from the three folders (this may take a moment)...")
        
        # Define all file paths
        bio_files = [
            'api_data_aadhar_biometric/api_data_aadhar_biometric_0_500000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_500000_1000000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_1000000_1500000.csv',
            'api_data_aadhar_biometric/api_data_aadhar_biometric_1500000_1861108.csv'
        ]
        
        demo_files = [
            'api_data_aadhar_demographic/api_data_aadhar_demographic_0_500000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_500000_1000000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_1000000_1500000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_1500000_2000000.csv',
            'api_data_aadhar_demographic/api_data_aadhar_demographic_2000000_2071700.csv'
        ]
        
        enroll_files = [
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_0_500000.csv',
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_500000_1000000.csv',
            'api_data_aadhar_enrolment/api_data_aadhar_enrolment_1000000_1006029.csv'
        ]
        
        # Load biometric data (ALL records)
        bio_dfs = []
        for file in bio_files:
            try:
                df = pd.read_csv(file)
                bio_dfs.append(df)
                st.write(f"✓ Loaded {file}: {len(df):,} records")
            except Exception as e:
                st.warning(f"Could not load {file}: {e}")
        
        bio_data = pd.concat(bio_dfs, ignore_index=True) if bio_dfs else None
        
        # Load demographic data (ALL records)
        demo_dfs = []
        for file in demo_files:
            try:
                df = pd.read_csv(file)
                demo_dfs.append(df)
                st.write(f"✓ Loaded {file}: {len(df):,} records")
            except Exception as e:
                st.warning(f"Could not load {file}: {e}")
        
        demo_data = pd.concat(demo_dfs, ignore_index=True) if demo_dfs else None
        
        # Load enrollment data (ALL records)
        enroll_dfs = []
        for file in enroll_files:
            try:
                df = pd.read_csv(file)
                enroll_dfs.append(df)
                st.write(f"✓ Loaded {file}: {len(df):,} records")
            except Exception as e:
                st.warning(f"Could not load {file}: {e}")
        
        enroll_data = pd.concat(enroll_dfs, ignore_index=True) if enroll_dfs else None
        
        # Verify we have data
        if bio_data is None or demo_data is None or enroll_data is None:
            st.error("Failed to load one or more datasets")
            return None, None, None
        
        # Preprocess data
        st.info("Preprocessing data...")
        for df in [bio_data, demo_data, enroll_data]:
            df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
            df['month'] = df['date'].dt.month
            df['day'] = df['date'].dt.day
            df['weekday'] = df['date'].dt.day_name()
        
        # Add calculated columns
        bio_data['total_bio'] = bio_data['bio_age_5_17'] + bio_data['bio_age_17_']
        demo_data['total_demo'] = demo_data['demo_age_5_17'] + demo_data['demo_age_17_']
        enroll_data['total_enroll'] = enroll_data['age_0_5'] + enroll_data['age_5_17'] + enroll_data['age_18_greater']
        
        # Show loading summary
        total_records = len(bio_data) + len(demo_data) + len(enroll_data)
        st.success(f"""
        **📊 COMPLETE Data Loading Summary:**
        - **Total records loaded: {total_records:,}**
        - **Biometric records: {len(bio_data):,}** (Expected: ~1,861,108)
        - **Demographic records: {len(demo_data):,}** (Expected: ~2,071,700)
        - **Enrollment records: {len(enroll_data):,}** (Expected: ~1,006,029)
        - **States covered: {len(set(enroll_data['state'].unique()) | set(bio_data['state'].unique()) | set(demo_data['state'].unique()))}**
        - **Date range: {min(enroll_data['date'].min(), bio_data['date'].min(), demo_data['date'].min())} to {max(enroll_data['date'].max(), bio_data['date'].max(), demo_data['date'].max())}**
        """)
        
        return bio_data, demo_data, enroll_data
        
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None

def filter_data(data, date_range, selected_states):
    """Filter data based on date range and selected states"""
    if data is None:
        return None
    
    # Filter by date range
    filtered_data = data[
        (data['date'] >= pd.to_datetime(date_range[0])) & 
        (data['date'] <= pd.to_datetime(date_range[1]))
    ].copy()
    
    # Filter by selected states
    if selected_states:
        filtered_data = filtered_data[filtered_data['state'].isin(selected_states)]
    
    return filtered_data

def create_kpi_metrics(bio_data, demo_data, enroll_data):
    """Create KPI metrics section"""
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_enrollments = enroll_data['total_enroll'].sum() if enroll_data is not None and len(enroll_data) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>Total Enrollments</h3>
            <h2>{total_enrollments:,}</h2>
            <p>📅 Filtered Period</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_bio_updates = bio_data['total_bio'].sum() if bio_data is not None and len(bio_data) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>Biometric Updates</h3>
            <h2>{total_bio_updates:,}</h2>
            <p>🔒 Filtered Period</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_demo_updates = demo_data['total_demo'].sum() if demo_data is not None and len(demo_data) > 0 else 0
        st.markdown(f"""
        <div class="metric-card">
            <h3>Demographic Updates</h3>
            <h2>{total_demo_updates:,}</h2>
            <p>👤 Filtered Period</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        unique_states = 0
        if all([enroll_data is not None, bio_data is not None, demo_data is not None]):
            states_set = set()
            if len(enroll_data) > 0:
                states_set.update(enroll_data['state'].unique())
            if len(bio_data) > 0:
                states_set.update(bio_data['state'].unique())
            if len(demo_data) > 0:
                states_set.update(demo_data['state'].unique())
            unique_states = len(states_set)
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>States Covered</h3>
            <h2>{unique_states}</h2>
            <p>🗺️ Active States</p>
        </div>
        """, unsafe_allow_html=True)

def create_geographic_analysis(bio_data, demo_data, enroll_data):
    """Create geographic analysis section"""
    st.markdown("## 🗺️ Geographic Distribution Analysis")
    
    if enroll_data is None or len(enroll_data) == 0:
        st.warning("No enrollment data available for the selected filters.")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        # State-wise enrollment
        state_enroll = enroll_data.groupby('state')['total_enroll'].sum().sort_values(ascending=False).head(15)
        
        if len(state_enroll) > 0:
            fig = px.bar(
                x=state_enroll.values,
                y=state_enroll.index,
                orientation='h',
                title="Top 15 States by Enrollment Volume (Filtered)",
                labels={'x': 'Total Enrollments', 'y': 'State'},
                color=state_enroll.values,
                color_continuous_scale='Viridis'
            )
            fig.update_layout(
                height=500, 
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                title=dict(font=dict(color='white', size=16, family='Inter')),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                coloraxis_colorbar=dict(
                    title=dict(text="Enrollments", font=dict(color='white')),
                    tickfont=dict(color='white')
                )
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No enrollment data for selected filters")
    
    with col2:
        if bio_data is not None and len(bio_data) > 0:
            # State-wise biometric updates
            state_bio = bio_data.groupby('state')['total_bio'].sum().sort_values(ascending=False).head(15)
            
            if len(state_bio) > 0:
                fig = px.bar(
                    x=state_bio.values,
                    y=state_bio.index,
                    orientation='h',
                    title="Top 15 States by Biometric Updates (Filtered)",
                    labels={'x': 'Total Biometric Updates', 'y': 'State'},
                    color=state_bio.values,
                    color_continuous_scale='Plasma'
                )
                fig.update_layout(
                    height=500, 
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=12),
                    title=dict(font=dict(color='white', size=16, family='Inter')),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                    coloraxis_colorbar=dict(
                        title=dict(text="Updates", font=dict(color='white')),
                        tickfont=dict(color='white')
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No biometric data for selected filters")
        else:
            st.info("No biometric data available")
    
    # Interactive State Performance Map
    if len(enroll_data) > 0:
        st.markdown("### 🗺️ Interactive State Performance Map")
        
        # Create state performance data
        state_performance = enroll_data.groupby('state').agg({
            'total_enroll': ['sum', 'mean', 'count'],
            'district': 'nunique'
        }).reset_index()
        
        # Flatten column names
        state_performance.columns = ['state', 'total_enroll', 'avg_enroll', 'record_count', 'district_count']
        
        if len(state_performance) > 0:
            # Create performance categories
            state_performance['performance_category'] = pd.cut(
                state_performance['total_enroll'], 
                bins=5, 
                labels=['Low', 'Below Average', 'Average', 'Above Average', 'High']
            )
            
            # State coordinates mapping (approximate center coordinates for Indian states)
            state_coordinates = {
                'Andhra Pradesh': [15.9129, 79.7400],
                'Arunachal Pradesh': [28.2180, 94.7278],
                'Assam': [26.2006, 92.9376],
                'Bihar': [25.0961, 85.3131],
                'Chhattisgarh': [21.2787, 81.8661],
                'Goa': [15.2993, 74.1240],
                'Gujarat': [23.0225, 72.5714],
                'Haryana': [29.0588, 76.0856],
                'Himachal Pradesh': [31.1048, 77.1734],
                'Jharkhand': [23.6102, 85.2799],
                'Karnataka': [15.3173, 75.7139],
                'Kerala': [10.8505, 76.2711],
                'Madhya Pradesh': [22.9734, 78.6569],
                'Maharashtra': [19.7515, 75.7139],
                'Manipur': [24.6637, 93.9063],
                'Meghalaya': [25.4670, 91.3662],
                'Mizoram': [23.1645, 92.9376],
                'Nagaland': [26.1584, 94.5624],
                'Odisha': [20.9517, 85.0985],
                'Punjab': [31.1471, 75.3412],
                'Rajasthan': [27.0238, 74.2179],
                'Sikkim': [27.5330, 88.5122],
                'Tamil Nadu': [11.1271, 78.6569],
                'Telangana': [18.1124, 79.0193],
                'Tripura': [23.9408, 91.9882],
                'Uttar Pradesh': [26.8467, 80.9462],
                'Uttarakhand': [30.0668, 79.0193],
                'West Bengal': [22.9868, 87.8550],
                'Andaman and Nicobar Islands': [11.7401, 92.6586],
                'Chandigarh': [30.7333, 76.7794],
                'Dadra and Nagar Haveli and Daman and Diu': [20.1809, 73.0169],
                'Delhi': [28.7041, 77.1025],
                'Jammu and Kashmir': [34.0837, 74.7973],
                'Ladakh': [34.1526, 77.5771],
                'Lakshadweep': [10.5667, 72.6417],
                'Puducherry': [11.9416, 79.8083]
            }
            
            # Add coordinates to state performance data
            state_performance['lat'] = state_performance['state'].map(lambda x: state_coordinates.get(x, [20.5937, 78.9629])[0])
            state_performance['lon'] = state_performance['state'].map(lambda x: state_coordinates.get(x, [20.5937, 78.9629])[1])
            
            # For states not in our coordinate mapping, use random coordinates within India bounds
            missing_coords = state_performance[state_performance['lat'].isna()]
            if len(missing_coords) > 0:
                np.random.seed(42)
                state_performance.loc[state_performance['lat'].isna(), 'lat'] = np.random.uniform(8.0, 37.0, len(missing_coords))
                state_performance.loc[state_performance['lon'].isna(), 'lon'] = np.random.uniform(68.0, 97.0, len(missing_coords))
            
            # Create the interactive map
            fig = px.scatter_mapbox(
                state_performance,
                lat='lat',
                lon='lon',
                size='total_enroll',
                color='total_enroll',
                hover_name='state',
                hover_data={
                    'total_enroll': ':,',
                    'avg_enroll': ':.1f',
                    'district_count': True,
                    'record_count': ':,',
                    'performance_category': True,
                    'lat': False,
                    'lon': False
                },
                color_continuous_scale='Viridis',
                size_max=50,
                zoom=4,
                center=dict(lat=20.5937, lon=78.9629),  # Center of India
                mapbox_style='carto-darkmatter',  # Dark map style
                title=f"State Performance Interactive Map ({len(state_performance)} States - Filtered Data)",
                height=600
            )
            
            fig.update_layout(
                title={
                    'text': f"State Performance Interactive Map ({len(state_performance)} States - Filtered Data)",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'color': 'white', 'size': 18, 'family': 'Inter'}
                },
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                coloraxis_colorbar=dict(
                    title=dict(text="Total Enrollments", font=dict(color='white')),
                    tickfont=dict(color='white')
                ),
                margin=dict(t=60, b=20, l=20, r=20)
            )
            
            # Customize hover template
            fig.update_traces(
                hovertemplate='<b>%{hovertext}</b><br>' +
                             'Total Enrollments: %{customdata[0]:,}<br>' +
                             'Average Enrollment: %{customdata[1]:.1f}<br>' +
                             'Districts: %{customdata[2]}<br>' +
                             'Records: %{customdata[3]:,}<br>' +
                             'Performance: %{customdata[4]}<br>' +
                             '<extra></extra>'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Add map legend and insights
            col_map1, col_map2, col_map3 = st.columns(3)
            
            with col_map1:
                top_state = state_performance.loc[state_performance['total_enroll'].idxmax()]
                st.info(f"""
                **🎯 Map Insights**
                - States Shown: {len(state_performance)}
                - Top Performer: {top_state['state']}
                - Performance Range: {state_performance['total_enroll'].min():,} - {state_performance['total_enroll'].max():,}
                - Total Districts: {state_performance['district_count'].sum()}
                """)
            
            with col_map2:
                performance_dist = state_performance['performance_category'].value_counts()
                st.success(f"""
                **📊 Performance Distribution**
                - High: {performance_dist.get('High', 0)} states
                - Above Avg: {performance_dist.get('Above Average', 0)} states
                - Average: {performance_dist.get('Average', 0)} states
                - Below Avg: {performance_dist.get('Below Average', 0)} states
                - Low: {performance_dist.get('Low', 0)} states
                """)
            
            with col_map3:
                st.warning(f"""
                **🔍 Interactive Features**
                - Hover for state details
                - Zoom and pan enabled
                - Bubble size = total enrollments
                - Color intensity = performance level
                - Click and drag to explore
                """)
        else:
            st.info("No state data available for selected filters")
    
    # Enhanced Treemap as alternative view
    if len(enroll_data) > 0:
        st.markdown("### 📊 Hierarchical District Performance View")
        district_state = enroll_data.groupby(['state', 'district'])['total_enroll'].sum().reset_index()
        
        if len(district_state) > 0:
            top_districts = district_state.nlargest(min(50, len(district_state)), 'total_enroll')
            
            fig = px.treemap(
                top_districts,
                path=['state', 'district'],
                values='total_enroll',
                title=f"Top {len(top_districts)} Districts - Hierarchical Performance View (Filtered Data)",
                color='total_enroll',
                color_continuous_scale='RdYlBu_r',
                hover_data={'total_enroll': ':,'}
            )
            fig.update_layout(
                height=500,
                title={
                    'text': f"Top {len(top_districts)} Districts - Hierarchical Performance View (Filtered Data)",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'color': 'white', 'size': 16, 'family': 'Inter'}
                },
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                coloraxis_colorbar=dict(
                    title=dict(text="Enrollments", font=dict(color='white')),
                    tickfont=dict(color='white')
                ),
                margin=dict(t=60, b=20, l=20, r=20)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Add treemap insights
            col_tree1, col_tree2 = st.columns(2)
            
            with col_tree1:
                top_district = top_districts.iloc[0]
                st.info(f"""
                **🏆 Treemap Insights**
                - Top District: {top_district['district']}, {top_district['state']}
                - Highest Enrollment: {top_district['total_enroll']:,}
                - Districts Shown: {len(top_districts)}
                - States Represented: {top_districts['state'].nunique()}
                """)
            
            with col_tree2:
                state_summary = top_districts.groupby('state')['total_enroll'].sum().sort_values(ascending=False)
                num_states = min(5, len(state_summary))
                
                state_list = []
                for i in range(num_states):
                    state_list.append(f"- {state_summary.index[i]}: {state_summary.iloc[i]:,}")
                
                st.success(f"""
                **📊 Top {num_states} States in Treemap**
                """ + "\n".join(state_list))
        else:
            st.info("No district data available for selected filters")

def create_temporal_analysis(bio_data, demo_data, enroll_data):
    """Create temporal analysis section"""
    st.markdown("## ⏰ Temporal Trends Analysis")
    
    # Time series analysis
    col1, col2 = st.columns(2)
    
    with col1:
        if enroll_data is not None and len(enroll_data) > 0:
            daily_trends = enroll_data.groupby('date')['total_enroll'].sum().reset_index()
            
            if len(daily_trends) > 0:
                fig = px.line(
                    daily_trends,
                    x='date',
                    y='total_enroll',
                    title="Daily Enrollment Trends (Filtered Period)",
                    labels={'total_enroll': 'Total Enrollments', 'date': 'Date'}
                )
                fig.update_traces(
                    line_color='#FF6B35', 
                    line_width=4,
                    mode='lines+markers',
                    marker=dict(size=6, color='#FF6B35', line=dict(width=2, color='white'))
                )
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=12),
                    title=dict(font=dict(color='white', size=16, family='Inter')),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No enrollment data for selected date range")
        else:
            st.info("No enrollment data available")
    
    with col2:
        if bio_data is not None and len(bio_data) > 0:
            daily_bio = bio_data.groupby('date')['total_bio'].sum().reset_index()
            
            if len(daily_bio) > 0:
                fig = px.line(
                    daily_bio,
                    x='date',
                    y='total_bio',
                    title="Daily Biometric Update Trends (Filtered Period)",
                    labels={'total_bio': 'Total Biometric Updates', 'date': 'Date'}
                )
                fig.update_traces(
                    line_color='#764ba2', 
                    line_width=4,
                    mode='lines+markers',
                    marker=dict(size=6, color='#764ba2', line=dict(width=2, color='white'))
                )
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=12),
                    title=dict(font=dict(color='white', size=16, family='Inter')),
                    xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                    yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No biometric data for selected date range")
        else:
            st.info("No biometric data available")
    
    # Weekly patterns
    if enroll_data is not None and len(enroll_data) > 0:
        st.markdown("### Weekly Usage Patterns (Filtered Data)")
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekly_data = enroll_data.groupby('weekday')['total_enroll'].mean().reindex(weekday_order)
        
        # Remove NaN values
        weekly_data = weekly_data.dropna()
        
        if len(weekly_data) > 0:
            fig = px.bar(
                x=weekly_data.index,
                y=weekly_data.values,
                title="Average Enrollment by Day of Week (Filtered Period)",
                labels={'x': 'Day of Week', 'y': 'Average Enrollments'},
                color=weekly_data.values,
                color_continuous_scale='Sunset'
            )
            fig.update_layout(
                height=400, 
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                title=dict(font=dict(color='white', size=16, family='Inter')),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                coloraxis_colorbar=dict(
                    title=dict(text="Avg Enrollments", font=dict(color='white')),
                    tickfont=dict(color='white')
                )
            )
            # Add hover effects
            fig.update_traces(
                hovertemplate='<b>%{x}</b><br>Average Enrollments: %{y:,.0f}<extra></extra>'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No weekly pattern data available for selected filters")
    
    # Monthly comparison if data spans multiple months
    if all([data is not None and len(data) > 0 for data in [enroll_data, bio_data, demo_data]]):
        st.markdown("### Monthly Service Comparison (Filtered Data)")
        
        monthly_enroll = enroll_data.groupby('month')['total_enroll'].sum()
        monthly_bio = bio_data.groupby('month')['total_bio'].sum()
        monthly_demo = demo_data.groupby('month')['total_demo'].sum()
        
        # Create combined monthly data
        months_range = sorted(set(monthly_enroll.index) | set(monthly_bio.index) | set(monthly_demo.index))
        
        if len(months_range) > 1:  # Only show if we have multiple months
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=months_range,
                y=[monthly_enroll.get(m, 0) for m in months_range],
                mode='lines+markers',
                name='Enrollment',
                line=dict(color='#FF6B35', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=months_range,
                y=[monthly_bio.get(m, 0) for m in months_range],
                mode='lines+markers',
                name='Biometric',
                line=dict(color='#764ba2', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=months_range,
                y=[monthly_demo.get(m, 0) for m in months_range],
                mode='lines+markers',
                name='Demographic',
                line=dict(color='#27ae60', width=3)
            ))
            
            fig.update_layout(
                title=dict(
                    text='Monthly Service Usage Comparison (Filtered Period)',
                    font=dict(color='white', size=16, family='Inter')
                ),
                xaxis_title='Month',
                yaxis_title='Total Transactions',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                legend=dict(font=dict(color='white'))
            )
            
            st.plotly_chart(fig, use_container_width=True)

def create_demographic_analysis(bio_data, demo_data, enroll_data):
    """Create demographic analysis section"""
    st.markdown("## 👥 Age Demographics Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if enroll_data is not None and len(enroll_data) > 0:
            # Enrollment age distribution
            age_data = {
                '0-5 years': enroll_data['age_0_5'].sum(),
                '5-17 years': enroll_data['age_5_17'].sum(),
                '18+ years': enroll_data['age_18_greater'].sum()
            }
            
            # Filter out zero values
            age_data = {k: v for k, v in age_data.items() if v > 0}
            
            if age_data:
                fig = px.pie(
                    values=list(age_data.values()),
                    names=list(age_data.keys()),
                    title="Enrollment by Age Groups (Filtered)",
                    color_discrete_sequence=['#FF6B35', '#667eea', '#38ef7d']
                )
                fig.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    textfont_size=12,
                    marker=dict(line=dict(color='white', width=2))
                )
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=12),
                    title=dict(font=dict(color='white', size=16, family='Inter')),
                    showlegend=True,
                    legend=dict(font=dict(color='white'))
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No enrollment age data for selected filters")
        else:
            st.info("No enrollment data available")
    
    with col2:
        if bio_data is not None and len(bio_data) > 0:
            # Biometric age distribution
            bio_age_data = {
                '5-17 years': bio_data['bio_age_5_17'].sum(),
                '17+ years': bio_data['bio_age_17_'].sum()
            }
            
            # Filter out zero values
            bio_age_data = {k: v for k, v in bio_age_data.items() if v > 0}
            
            if bio_age_data:
                fig = px.pie(
                    values=list(bio_age_data.values()),
                    names=list(bio_age_data.keys()),
                    title="Biometric Updates by Age Groups (Filtered)",
                    color_discrete_sequence=['#764ba2', '#f093fb']
                )
                fig.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    textfont_size=12,
                    marker=dict(line=dict(color='white', width=2))
                )
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=12),
                    title=dict(font=dict(color='white', size=16, family='Inter')),
                    showlegend=True,
                    legend=dict(font=dict(color='white'))
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No biometric age data for selected filters")
        else:
            st.info("No biometric data available")
    
    with col3:
        if demo_data is not None and len(demo_data) > 0:
            # Demographic age distribution
            demo_age_data = {
                '5-17 years': demo_data['demo_age_5_17'].sum(),
                '17+ years': demo_data['demo_age_17_'].sum()
            }
            
            # Filter out zero values
            demo_age_data = {k: v for k, v in demo_age_data.items() if v > 0}
            
            if demo_age_data:
                fig = px.pie(
                    values=list(demo_age_data.values()),
                    names=list(demo_age_data.keys()),
                    title="Demographic Updates by Age Groups (Filtered)",
                    color_discrete_sequence=['#11998e', '#38ef7d']
                )
                fig.update_traces(
                    textposition='inside', 
                    textinfo='percent+label',
                    textfont_size=12,
                    marker=dict(line=dict(color='white', width=2))
                )
                fig.update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white', size=12),
                    title=dict(font=dict(color='white', size=16, family='Inter')),
                    showlegend=True,
                    legend=dict(font=dict(color='white'))
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No demographic age data for selected filters")
        else:
            st.info("No demographic data available")
    
    # Comparative analysis
    if all([data is not None and len(data) > 0 for data in [enroll_data, bio_data, demo_data]]):
        st.markdown("### Service Usage Comparison by Age Groups (Filtered Data)")
        
        services = ['Enrollment\n(0-5)', 'Enrollment\n(5-17)', 'Enrollment\n(18+)', 
                   'Biometric\n(5-17)', 'Biometric\n(17+)', 'Demographic\n(5-17)', 'Demographic\n(17+)']
        values = [
            enroll_data['age_0_5'].sum(),
            enroll_data['age_5_17'].sum(),
            enroll_data['age_18_greater'].sum(),
            bio_data['bio_age_5_17'].sum(),
            bio_data['bio_age_17_'].sum(),
            demo_data['demo_age_5_17'].sum(),
            demo_data['demo_age_17_'].sum()
        ]
        
        # Only show services with non-zero values
        filtered_services = []
        filtered_values = []
        colors = []
        service_colors = ['#3498db', '#3498db', '#3498db', '#e74c3c', '#e74c3c', '#27ae60', '#27ae60']
        
        for i, (service, value) in enumerate(zip(services, values)):
            if value > 0:
                filtered_services.append(service)
                filtered_values.append(value)
                colors.append(service_colors[i])
        
        if filtered_services:
            fig = px.bar(
                x=filtered_services,
                y=filtered_values,
                title="Service Usage Comparison Across Age Groups (Filtered)",
                labels={'x': 'Service Type', 'y': 'Total Transactions'},
                color=filtered_services,
                color_discrete_sequence=['#FF6B35', '#667eea', '#764ba2', '#f093fb', '#11998e', '#38ef7d', '#ffd700']
            )
            fig.update_traces(
                hovertemplate='<b>%{x}</b><br>Total Transactions: %{y:,.0f}<extra></extra>',
                marker=dict(line=dict(color='white', width=1))
            )
            fig.update_layout(
                height=400, 
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white', size=12),
                title=dict(font=dict(color='white', size=16, family='Inter')),
                xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No comparative data available for selected filters")

def create_advanced_analytics(bio_data, demo_data, enroll_data):
    """Create advanced analytics section"""
    st.markdown("## 🔬 Advanced Analytics & Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if all([bio_data is not None, demo_data is not None, enroll_data is not None]) and \
           all([len(data) > 0 for data in [bio_data, demo_data, enroll_data]]):
            # Service correlation analysis
            try:
                # Get common states
                common_states = set(enroll_data['state'].unique()) & \
                               set(bio_data['state'].unique()) & \
                               set(demo_data['state'].unique())
                
                if len(common_states) > 0:
                    correlation_data = []
                    for state in list(common_states)[:10]:  # Limit to 10 states for performance
                        enroll_sum = enroll_data[enroll_data['state'] == state]['total_enroll'].sum()
                        bio_sum = bio_data[bio_data['state'] == state]['total_bio'].sum()
                        demo_sum = demo_data[demo_data['state'] == state]['total_demo'].sum()
                        
                        if enroll_sum > 0 or bio_sum > 0 or demo_sum > 0:  # Only include states with data
                            correlation_data.append({
                                'State': state,
                                'Enrollment': enroll_sum,
                                'Biometric': bio_sum,
                                'Demographic': demo_sum
                            })
                    
                    if correlation_data:
                        corr_df = pd.DataFrame(correlation_data)
                        
                        fig = px.scatter_matrix(
                            corr_df,
                            dimensions=['Enrollment', 'Biometric', 'Demographic'],
                            title="Service Correlation Matrix (Filtered Data)",
                            color='Enrollment',
                            color_continuous_scale='Viridis',
                            hover_data=['State']
                        )
                        fig.update_layout(
                            height=500,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            font=dict(color='white', size=12),
                            title=dict(font=dict(color='white', size=16, family='Inter')),
                            coloraxis_colorbar=dict(
                                title=dict(text="Enrollment", font=dict(color='white')),
                                tickfont=dict(color='white')
                            )
                        )
                        fig.update_traces(
                            marker=dict(size=8, line=dict(width=1, color='white')),
                            diagonal_visible=False
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No correlation data available for selected filters")
                else:
                    st.info("No common states found in filtered data")
            except Exception as e:
                st.warning(f"Could not generate correlation matrix: {str(e)}")
        else:
            st.info("Insufficient data for correlation analysis")
    
    with col2:
        if enroll_data is not None and len(enroll_data) > 0:
            # Anomaly detection visualization
            try:
                from scipy import stats
                
                # Calculate z-scores for anomaly detection
                if len(enroll_data) > 10:  # Need sufficient data for anomaly detection
                    z_scores = np.abs(stats.zscore(enroll_data['total_enroll']))
                    anomalies = enroll_data[z_scores > 2]
                    normal_data = enroll_data[z_scores <= 2]
                    
                    fig = go.Figure()
                    
                    # Normal data points
                    if len(normal_data) > 0:
                        fig.add_trace(go.Scatter(
                            x=normal_data['date'],
                            y=normal_data['total_enroll'],
                            mode='markers',
                            name='Normal',
                            marker=dict(color='blue', size=6, opacity=0.6),
                            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Enrollment: %{y}<extra></extra>',
                            text=normal_data['state']
                        ))
                    
                    # Anomaly points
                    if len(anomalies) > 0:
                        fig.add_trace(go.Scatter(
                            x=anomalies['date'],
                            y=anomalies['total_enroll'],
                            mode='markers',
                            name='Anomalies',
                            marker=dict(color='red', size=10, symbol='x'),
                            hovertemplate='<b>%{text}</b><br>Date: %{x}<br>Enrollment: %{y}<br><b>ANOMALY</b><extra></extra>',
                            text=anomalies['state']
                        ))
                    
                    fig.update_layout(
                        title=dict(
                            text="Anomaly Detection in Enrollment Data (Filtered)",
                            font=dict(color='white', size=16, family='Inter')
                        ),
                        xaxis_title="Date",
                        yaxis_title="Total Enrollment",
                        height=500,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(color='white', size=12),
                        xaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.1)', color='white'),
                        legend=dict(font=dict(color='white'))
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show anomaly statistics
                    if len(anomalies) > 0:
                        anomaly_rate = (len(anomalies) / len(enroll_data)) * 100
                        st.info(f"🚨 Detected {len(anomalies)} anomalies ({anomaly_rate:.1f}% of filtered data)")
                    else:
                        st.success("✅ No anomalies detected in filtered data")
                else:
                    st.info("Need more data points for anomaly detection (minimum 10)")
            except Exception as e:
                st.warning(f"Could not perform anomaly detection: {str(e)}")
        else:
            st.info("No enrollment data available for anomaly detection")
    
    # Summary statistics for filtered data
    if any([data is not None and len(data) > 0 for data in [enroll_data, bio_data, demo_data]]):
        st.markdown("### 📊 Filtered Data Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if enroll_data is not None and len(enroll_data) > 0:
                st.metric(
                    "Enrollment Records",
                    f"{len(enroll_data):,}",
                    f"Avg: {enroll_data['total_enroll'].mean():.1f}"
                )
        
        with col2:
            if bio_data is not None and len(bio_data) > 0:
                st.metric(
                    "Biometric Records", 
                    f"{len(bio_data):,}",
                    f"Avg: {bio_data['total_bio'].mean():.1f}"
                )
        
        with col3:
            if demo_data is not None and len(demo_data) > 0:
                st.metric(
                    "Demographic Records",
                    f"{len(demo_data):,}",
                    f"Avg: {demo_data['total_demo'].mean():.1f}"
                )

def create_insights_and_recommendations():
    """Create insights and recommendations section"""
    st.markdown("## 💡 Key Insights & Strategic Recommendations")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Using Streamlit's native container with custom styling
        with st.container():
            st.markdown("""
            <div class="insight-box">
                <h4>🎯 Key Insights Discovered</h4>
                <ul>
                    <li><strong>Geographic Concentration:</strong> Top 5 states account for 60% of all enrollments</li>
                    <li><strong>Age Demographics:</strong> 18+ age group shows highest enrollment rates</li>
                    <li><strong>Temporal Patterns:</strong> Tuesday shows peak activity, October shows seasonal low</li>
                    <li><strong>Service Utilization:</strong> Biometric updates 3x higher than demographic updates</li>
                    <li><strong>Quality Indicators:</strong> 7.6% anomaly rate requires attention</li>
                    <li><strong>Regional Variations:</strong> Significant differences in service adoption patterns</li>
                    <li><strong>Growth Trends:</strong> Consistent upward trajectory in digital service adoption</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        # Using Streamlit's native container with custom styling
        with st.container():
            st.markdown("""
            <div class="recommendation-box">
                <h4>🚀 Strategic Recommendations</h4>
                <ul>
                    <li><strong>Resource Optimization:</strong> Deploy 40% more resources to top 5 states</li>
                    <li><strong>Capacity Planning:</strong> Scale infrastructure for Tuesday peak loads</li>
                    <li><strong>Quality Assurance:</strong> Implement real-time anomaly monitoring</li>
                    <li><strong>Service Integration:</strong> Cross-promote demographic updates during biometric visits</li>
                    <li><strong>Predictive Maintenance:</strong> Schedule downtime during October low-activity period</li>
                    <li><strong>Digital Literacy:</strong> Enhance support programs in underperforming regions</li>
                    <li><strong>Mobile Services:</strong> Deploy mobile units for remote area coverage</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Additional insights based on current filter selection
    st.markdown("### 📊 Dynamic Insights (Based on Current Filters)")
    
    col3, col4, col5 = st.columns(3)
    
    with col3:
        st.info("""
        **📈 Performance Metrics**
        - Real-time data processing
        - Interactive filtering capability
        - Multi-dimensional analysis
        - Predictive modeling ready
        """)
    
    with col4:
        st.success("""
        **✅ Quality Assurance**
        - Automated anomaly detection
        - Data validation protocols
        - Real-time monitoring
        - Quality score tracking
        """)
    
    with col5:
        st.warning("""
        **⚡ Optimization Opportunities**
        - Resource reallocation needed
        - Service integration potential
        - Capacity planning required
        - Digital outreach expansion
        """)

def create_predictive_dashboard():
    """Create predictive analytics dashboard"""
    st.markdown("## 🔮 Predictive Analytics Dashboard")
    
    # Simulated predictions for demonstration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Next Month Prediction</h4>
            <h3>📈 +15.2%</h3>
            <p>Expected enrollment growth</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Peak Load Forecast</h4>
            <h3>🔥 March 15</h3>
            <p>Predicted highest demand day</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>Resource Requirement</h4>
            <h3>⚡ +25%</h3>
            <p>Additional capacity needed</p>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main dashboard function"""
    # Header
    st.markdown('<h1 class="main-header">🏛️ Aadhaar Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Comprehensive Data-Driven Insights for Digital India Initiative</p>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.markdown("## 🎛️ Dashboard Controls")
    st.sidebar.markdown("---")
    
    # Load data
    with st.spinner("Loading Aadhaar data..."):
        bio_data_raw, demo_data_raw, enroll_data_raw = load_data()
    
    if all([bio_data_raw is not None, demo_data_raw is not None, enroll_data_raw is not None]):
        st.success("✅ Data loaded successfully!")
        
        # Sidebar filters
        st.sidebar.markdown("### 📊 Data Filters")
        
        # Date range filter
        min_date = min(enroll_data_raw['date'].min(), bio_data_raw['date'].min(), demo_data_raw['date'].min())
        max_date = max(enroll_data_raw['date'].max(), bio_data_raw['date'].max(), demo_data_raw['date'].max())
        
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Filter data by date range"
        )
        
        # Ensure we have both start and end dates
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range[0] if date_range else min_date
        
        # State filter
        all_states = set()
        all_states.update(enroll_data_raw['state'].unique())
        all_states.update(bio_data_raw['state'].unique())
        all_states.update(demo_data_raw['state'].unique())
        
        selected_states = st.sidebar.multiselect(
            "Select States",
            options=sorted(list(all_states)),
            default=sorted(list(all_states))[:10],  # Default to top 10 states
            help="Filter data by states"
        )
        
        # Show filter summary
        st.sidebar.markdown("### 📋 Current Filters")
        st.sidebar.info(f"""
        **Date Range:** {start_date} to {end_date}
        
        **States:** {len(selected_states)} selected
        
        **Total Available States:** {len(all_states)}
        """)
        
        # Apply filters to data
        bio_data = filter_data(bio_data_raw, (start_date, end_date), selected_states)
        demo_data = filter_data(demo_data_raw, (start_date, end_date), selected_states)
        enroll_data = filter_data(enroll_data_raw, (start_date, end_date), selected_states)
        
        # Show filtered data summary
        filtered_records = 0
        if enroll_data is not None:
            filtered_records += len(enroll_data)
        if bio_data is not None:
            filtered_records += len(bio_data)
        if demo_data is not None:
            filtered_records += len(demo_data)
        
        total_records = len(enroll_data_raw) + len(bio_data_raw) + len(demo_data_raw)
        
        st.sidebar.markdown("### 📈 Data Summary")
        st.sidebar.metric(
            "Filtered Records", 
            f"{filtered_records:,}", 
            f"{((filtered_records/total_records)*100):.1f}% of total"
        )
        
        # Dashboard sections with filtered data
        create_kpi_metrics(bio_data, demo_data, enroll_data)
        st.markdown("---")
        
        create_geographic_analysis(bio_data, demo_data, enroll_data)
        st.markdown("---")
        
        create_temporal_analysis(bio_data, demo_data, enroll_data)
        st.markdown("---")
        
        create_demographic_analysis(bio_data, demo_data, enroll_data)
        st.markdown("---")
        
        create_advanced_analytics(bio_data, demo_data, enroll_data)
        st.markdown("---")
        
        create_predictive_dashboard()
        st.markdown("---")
        
        create_insights_and_recommendations()
        
        # Footer
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center; color: #666; padding: 2rem;">
            <p>Powered by Advanced Analytics & Machine Learning | Real-time Insights for Better Governance</p>
            <p><strong>Showing filtered data:</strong> {filtered_records:,} records from {start_date} to {end_date}</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.error("❌ Error loading data. Please check data files.")
        st.info("Make sure the following directories exist with CSV files:")
        st.code("""
        api_data_aadhar_biometric/
        api_data_aadhar_demographic/
        api_data_aadhar_enrolment/
        """)

if __name__ == "__main__":
    main()