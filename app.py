import streamlit as st
import fastf1
import fastf1.plotting  # Import the official F1 plotting utility matrix
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import os

# Set Tab Metadata Configuration
st.set_page_config(page_title="F1 Pit Wall Intelligence", layout="wide")

# High-Gloss F1 Theme & Wallpaper Design Matrix
st.markdown("""
    <style>
    /* Premium Carbon-Grid Wallpaper Backdrop */
    .stApp {
        background-color: #0B0C0E;
        background-image: 
            linear-gradient(30deg, #121417 12%, transparent 12.5%, transparent 87%, #121417 87.5%, #121417),
            linear-gradient(150deg, #121417 12%, transparent 12.5%, transparent 87%, #121417 87.5%, #121417),
            linear-gradient(300deg, #121417 12%, transparent 12.5%, transparent 87%, #121417 87.5%, #121417),
            linear-gradient(60deg, #121417 25%, transparent 25.5%, transparent 75%, #121417 75.5%, #121417),
            linear-gradient(240deg, #121417 25%, transparent 25.5%, transparent 75%, #121417 75.5%, #121417);
        background-size: 40px 70px;
        background-position: 0 0, 0 0, 20px 35px, 20px 35px, 0 0;
    }
    
    /* Metrics value telemetry font configuration */
    div[data-testid="stMetricValue"] {
        font-size: 38px !important;
        font-weight: 900 !important;
        color: #FFFFFF !important;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Elegant Sidebar Border Line */
    div[data-testid="stSidebar"] {
        border-right: 3px solid #FF1801;
        background-color: #0A0B0D !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main Dashboard Title Header Section
st.markdown("<h1 style='color: #FFFFFF; font-weight: 900; letter-spacing: -1.5px; margin-bottom: 5px;'>🏎️ FORMULA 1 PIT WALL INTELLIGENCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #A0A5AE; margin-top: -10px; font-weight: 500;'>Proprietary computational telemetry deck pulling continuous streaming arrays.</p>", unsafe_allow_html=True)
st.markdown("<div style='border-bottom: 3px solid #FF1801; width: 100%; margin-bottom: 30px;'></div>", unsafe_allow_html=True)

# Local Storage Engine Configuration
if not os.path.exists('f1_cache'):
    os.makedirs('f1_cache')
fastf1.Cache.enable_cache('f1_cache')

# Sidebar Control Architecture
st.sidebar.markdown("<h2 style='color: #FF1801; font-weight: 900; margin-bottom: 15px;'>📊 RACE CONTROL</h2>", unsafe_allow_html=True)
year = st.sidebar.selectbox("Select Season", [2026, 2025, 2024, 2023], index=1) # Set default to loaded 2025 data
location = st.sidebar.text_input("Track Circuit Location", "Monaco")
session_type = st.sidebar.selectbox("Session Type", ["R", "Q"], format_func=lambda x: "Race" if x == "R" else "Qualifying", index=1)

# Integrated Glossary Expander inside Sidebar
st.sidebar.markdown("<div style='border-top: 2px solid #22252A; margin: 20px 0;'></div>", unsafe_allow_html=True)
with st.sidebar.expander("📖 TELEMETRY DICTIONARY"):
    st.markdown("""
    **Aggression Index:**
    Measures how quickly a driver stamps on/off throttle inputs. Over 7.0 means snappy qualifying trim; under 4.0 means smooth cornering/tyre saving.
    
    **V-Max:**
    Top speed hit at deep straight marker.
    
    **Velocity Profile:**
    Continuous lines tracking speed versus physical track position meters.
    """)

drivers_list, session_meta = [], None
try:
    session = fastf1.get_session(year, location, session_type)
    session.load(telemetry=False, laps=True, weather=False, messages=False)
    drivers_list = session.laps['Driver'].unique().tolist()
except Exception as e:
    st.error(f"Error establishing hardware telemetry link: {e}")

if drivers_list:
    st.sidebar.markdown("<div style='border-top: 2px solid #22252A; margin: 20px 0;'></div>", unsafe_allow_html=True)
    st.sidebar.markdown("<h3 style='color: #FFFFFF; font-weight: 800; margin-bottom: 15px;'>🎯 DRIVER INTERCEPTS</h3>", unsafe_allow_html=True)
    driver1 = st.sidebar.selectbox("Primary Target Driver", drivers_list, index=0)
    driver2 = st.sidebar.selectbox("Comparison Target Driver", drivers_list, index=min(1, len(drivers_list)-1))

    @st.cache_data(show_spinner="🧮 Demultiplexing spatial sensor arrays...")
    def get_telemetry_data(year, location, session_type, d1, d2):
        session = fastf1.get_session(year, location, session_type)
        session.load(telemetry=True, laps=True, weather=False, messages=False)
        lap1 = session.laps.pick_driver(d1).pick_fastest()
        lap2 = session.laps.pick_driver(d2).pick_fastest()
        
        # Pull dynamic hexadecimal color profiles from team tags safely
        try:
            c1 = fastf1.plotting.team_color(lap1['Team'])
        except:
            c1 = '#FF1801' # Fallback default F1 Red
            
        try:
            c2 = fastf1.plotting.team_color(lap2['Team'])
            if c1 == c2: # If teammate comparison, offset colors slightly
                c2 = '#E1E4E6'
        except:
            c2 = '#E1E4E6' # Fallback default metallic grey
            
        return (lap1.get_telemetry().add_distance(), 
                lap2.get_telemetry().add_distance(), 
                lap1, lap2, c1, c2)

    try:
        tel1, tel2, full_lap1, full_lap2, color1, color2 = get_telemetry_data(year, location, session_type, driver1, driver2)
        
        # Compute Advanced Aggression Scores
        agg1 = np.abs(np.diff(tel1['Throttle'])).mean() * 10
        agg2 = np.abs(np.diff(tel2['Throttle'])).mean() * 10

        # --- DATASTREAM CARDS ROW (DYNAMCIALLY COLORED BY TEAM ACCENTS) ---
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"<div style='background-color: rgba(26,29,34,0.9); border-left: 5px solid {color1}; padding: 15px; border-radius: 4px; margin-bottom: 10px;'>"
                        f"<h4 style='margin:0; color:#FFFFFF; font-weight:800; font-size:16px;'>📊 DATASTREAM: {driver1} ({full_lap1['Team']})</h4></div>", unsafe_allow_html=True)
            sub_col1, sub_col2, sub_col3 = st.columns(3)
            sub_col1.metric(label="Aggression Profile", value=f"{agg1:.2f} / 10")
            sub_col2.metric(label="V-Max Velocity", value=f"{int(tel1['Speed'].max())} km/h")
            sub_col3.metric(label="Sector 1 Delta", value=f"{full_lap1['Sector1Time'].total_seconds():.3f}s")
            
        with col2:
            st.markdown(f"<div style='background-color: rgba(26,29,34,0.9); border-left: 5px solid {color2}; padding: 15px; border-radius: 4px; margin-bottom: 10px;'>"
                        f"<h4 style='margin:0; color:#FFFFFF; font-weight:800; font-size:16px;'>📊 DATASTREAM: {driver2} ({full_lap2['Team']})</h4></div>", unsafe_allow_html=True)
            sub_col4, sub_col5, sub_col6 = st.columns(3)
            sub_col4.metric(label="Aggression Profile", value=f"{agg2:.2f} / 10")
            sub_col5.metric(label="V-Max Velocity", value=f"{int(tel2['Speed'].max())} km/h")
            sub_col6.metric(label="Sector 1 Delta", value=f"{full_lap2['Sector1Time'].total_seconds():.3f}s")

        # --- TELEMETRY TRACES SUBPLOTS ---
        st.markdown("<h3 style='color: #FFFFFF; font-weight: 800; margin-top: 30px;'>📈 CONTINUOUS LAP VELOCITY PROFILES</h3>", unsafe_allow_html=True)
        
        fig_traces = go.Figure()
        fig_traces.add_trace(go.Scatter(x=tel1['Distance'], y=tel1['Speed'], name=driver1, line=dict(color=color1, width=2.5)))
        fig_traces.add_trace(go.Scatter(x=tel2['Distance'], y=tel2['Speed'], name=driver2, line=dict(color=color2, width=2, dash='dot')))
        fig_traces.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,17,20,0.6)',
            xaxis=dict(title="Distance Around Circuit (meters)", showgrid=True, gridcolor='#22252A'),
            yaxis=dict(title="Velocity (km/h)", showgrid=True, gridcolor='#22252A'),
            height=300,
            margin=dict(l=50, r=20, t=10, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_traces, use_container_width=True)

        # --- SPATIAL FIELD ARRAYS ---
        st.markdown("<div style='border-bottom: 2px solid #22252A; width: 100%; margin: 35px 0;'></div>", unsafe_allow_html=True)
        
        map_col, graph_col = st.columns([3, 2])
        
        with map_col:
            st.markdown("<h3 style='color: #FFFFFF; font-weight: 800; margin-bottom: 15px;'>📍 SPATIAL TRACK VELOCITY HEATMAP</h3>", unsafe_allow_html=True)
            fig_map = px.scatter(
                tel1, x="X", y="Y", color="Speed",
                color_continuous_scale=["#15181C", color1, "#FFD700"],
                hover_data=["Speed", "Throttle", "Brake", "nGear"]
            )
            fig_map.update_layout(
                height=500, 
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=0, b=0)
            )
            fig_map.update_yaxes(scaleanchor="x", scaleratio=1)
            st.plotly_chart(fig_map, use_container_width=True)
            
        with graph_col:
            st.markdown("<h3 style='color: #FFFFFF; font-weight: 800; margin-bottom: 15px;'>📊 THROTTLE FREQUENCY COMPRESSION</h3>", unsafe_allow_html=True)
            fig_metrics = go.Figure(go.Bar(
                x=[agg1, agg2],
                y=[driver1, driver2],
                orientation='h',
                marker=dict(color=[color1, color2]),
                text=[f"{agg1:.2f} Index", f"{agg2:.2f} Index"],
                textposition='auto',
                textfont=dict(color='#000000', weight='bold')
            ))
            fig_metrics.update_layout(
                template="plotly_dark",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=450,
                margin=dict(l=40, r=20, t=20, b=20),
                xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_metrics, use_container_width=True)

    except Exception as e:
        st.warning(f"Error rendering time-series visual components: {e}")