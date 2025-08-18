import streamlit as st
from utils.page_config import set_page_config
from utils.i18n import get_translations
t = get_translations()
set_page_config(t.get("truck_tracker", "Truck Tracker"))

from streamlit_folium import st_folium
import folium
from geopy.distance import geodesic
from folium.plugins import HeatMap
from components.sidebar import show_sidebar
from datetime import datetime

t = get_translations()

# Check authentication
if not st.session_state.get('authenticated', False):
    st.warning(t.get("please_login_first", "Please login first"))
    st.stop()

# Hide default sidebar navigation
st.markdown('''
    <style>
        [data-testid="stSidebarNav"] {display: none !important;}
    </style>
''', unsafe_allow_html=True)

# Show custom sidebar
show_sidebar()

st.title("🚛 " + t.get("truck_tracker", "Truck Emissions Tracker"))

# Vehicle and fuel selection
col1, col2 = st.columns(2)
with col1:
    vehicle_type = st.selectbox(t.get("vehicle_type", "Vehicle Type"), [t.get("light_truck", "Light Truck"), t.get("medium_truck", "Medium Truck"), t.get("heavy_truck", "Heavy Truck")])
with col2:
    fuel_type = st.selectbox(t.get("fuel_type", "Fuel Type"), [t.get("diesel", "Diesel"), t.get("gasoline", "Gasoline"), t.get("lpg", "LPG")])

# Emission factors (kg CO2 per km)
EMISSION_FACTORS = {
    "Light Truck": {"Diesel": 0.25, "Gasoline": 0.29, "LPG": 0.21},
    "Medium Truck": {"Diesel": 0.35, "Gasoline": 0.40, "LPG": 0.30},
    "Heavy Truck": {"Diesel": 0.45, "Gasoline": 0.50, "LPG": 0.40}
}

# Initialize session state
if 'map_points' not in st.session_state:
    st.session_state.map_points = {'start': None, 'end': None, 'selecting': None}

# Create map with picker functionality
# Center map on Tunisia
m = folium.Map(location=[34.0, 9.0], zoom_start=7)

# Add cursor style when selecting
if st.session_state.map_points['selecting']:
    m.get_root().html.add_child(folium.Element("""
    <style>
        .leaflet-container {
            cursor: crosshair !important;
        }
    </style>
    """))

# Add existing markers
if st.session_state.map_points['start']:
    folium.Marker(
        st.session_state.map_points['start'],
        popup="Start Point",
        icon=folium.Icon(color='green', icon='flag')
    ).add_to(m)

if st.session_state.map_points['end']:
    folium.Marker(
        st.session_state.map_points['end'],
        popup="End Point",
        icon=folium.Icon(color='red', icon='flag')
    ).add_to(m)
    
    if st.session_state.map_points['start']:
        folium.PolyLine(
            [st.session_state.map_points['start'], st.session_state.map_points['end']],
            color="blue",
            weight=2.5,
            opacity=1
        ).add_to(m)

# Custom CSS for full-width folium map
st.markdown('''
    <style>
    .full-width-map .folium-map {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        box-shadow: none !important;
        border-radius: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .full-width-map iframe {
        width: 100% !important;
        min-width: 100% !important;
        max-width: 100% !important;
        border: none !important;
    }
    </style>
''', unsafe_allow_html=True)

# Display map at 100% width
# Display map at 100% width
st.markdown('''
    <style>
    /* Remove extra margin below folium map */
    .element-container:has(.folium-map) {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    </style>
''', unsafe_allow_html=True)
map_data = st_folium(
    m,
    width='100%',
    height=500,
    returned_objects=["last_clicked"],
    key="truck_tracker_map"
)

# Selection buttons with visual feedback
st.markdown("### " + t.get("select_points", "Select Points"))
cols = st.columns(3)
with cols[0]:
    if st.button("📍 " + t.get("start_point", "Start Point"), key="btn_start", disabled=bool(st.session_state.map_points['selecting'] == 'start')):
        st.session_state.map_points['selecting'] = 'start'
        st.rerun()

with cols[1]:
    if st.button("📍 " + t.get("end_point", "End Point"), key="btn_end", disabled=bool(st.session_state.map_points['selecting'] == 'end')):
        st.session_state.map_points['selecting'] = 'end'
        st.rerun()

with cols[2]:
    if st.button("🔄 Clear All", key="btn_clear"):
        st.session_state.map_points = {'start': None, 'end': None, 'selecting': None}
        st.rerun()

# Handle map clicks
# Tunisia bounding box
TUNISIA_BOUNDS = {
    "min_lat": 30.2,
    "max_lat": 37.6,
    "min_lng": 7.5,
    "max_lng": 11.6
}

if map_data.get("last_clicked") and st.session_state.map_points['selecting']:
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]
    if (TUNISIA_BOUNDS["min_lat"] <= lat <= TUNISIA_BOUNDS["max_lat"] and
        TUNISIA_BOUNDS["min_lng"] <= lng <= TUNISIA_BOUNDS["max_lng"]):
        point_type = st.session_state.map_points['selecting']
        st.session_state.map_points[point_type] = [lat, lng]
        st.session_state.map_points['selecting'] = None
        st.rerun()
    else:
        st.warning(t.get("please_select_point_tunisia", "Please select a point inside Tunisia."))

# Auto-calculate when both points are set
if st.session_state.map_points['start'] and st.session_state.map_points['end']:
    distance = geodesic(
        st.session_state.map_points['start'],
        st.session_state.map_points['end']
    ).kilometers
    
    vehicle = st.session_state.get('selected_vehicle', 'Medium Truck')
    fuel = st.session_state.get('selected_fuel', 'Diesel')
    emission_factor = EMISSION_FACTORS[vehicle][fuel]
    
    emissions = distance * emission_factor
    
    # Create a new map for heatmap visualization centered on Tunisia
    m_heat = folium.Map(location=[34.0, 9.0], zoom_start=7)
    # Optionally: fix bounds to Tunisia
    m_heat.fit_bounds([[30.2, 7.5], [37.6, 11.6]])
    
    # Generate simulated alternative routes with different emissions
    alt_routes = [
        {'path': [st.session_state.map_points['start'], st.session_state.map_points['end']], 'emissions': emissions},
        {'path': [
            st.session_state.map_points['start'],
            [st.session_state.map_points['start'][0]+0.2, st.session_state.map_points['start'][1]+0.1],
            [st.session_state.map_points['end'][0]-0.1, st.session_state.map_points['end'][1]-0.2],
            st.session_state.map_points['end']
        ], 'emissions': emissions*0.9},  # 10% better
        {'path': [
            st.session_state.map_points['start'],
            [st.session_state.map_points['start'][0]-0.1, st.session_state.map_points['start'][1]+0.2],
            [st.session_state.map_points['end'][0]+0.2, st.session_state.map_points['end'][1]-0.1],
            st.session_state.map_points['end']
        ], 'emissions': emissions*1.1}   # 10% worse
    ]
    
    # Prepare heatmap data (weighted by emissions)
    heat_data = []
    for route in alt_routes:
        for point in route['path']:
            heat_data.append(point + [route['emissions']])
    
    # Add heatmap layer
    HeatMap(heat_data, radius=15, blur=10, min_opacity=0.5).add_to(m_heat)
    
    # Add route lines (green=best, red=worst)
    for i, route in enumerate(alt_routes):
        color = 'green' if i == 1 else ('red' if i == 2 else 'blue')
        folium.PolyLine(
            route['path'],
            color=color,
            weight=2.5,
            opacity=1,
            popup=f"{route['emissions']:.2f} kg CO2"
        ).add_to(m_heat)
    
    # Add markers
    folium.Marker(st.session_state.map_points['start'], popup="Start").add_to(m_heat)
    folium.Marker(st.session_state.map_points['end'], popup="End").add_to(m_heat)
    
    # Display heatmap
    st.subheader("🌡️ " + t.get("route_emissions_heatmap", "Route Emissions Heatmap"))
    st.caption(t.get("green_routes_efficient", "Green routes are more efficient, red routes are less efficient"))
    st_folium(m_heat, width='100%', height=500)
    
    # Show calculation results
    st.success(f"""
    **{t.get('route_calculated', 'Route Calculated')}**
    - {t.get('distance', 'Distance')}: {distance:.2f} km
    - {t.get('vehicle', 'Vehicle')}: {vehicle} ({fuel})
    - {t.get('co2_emissions', 'CO2 Emissions')}: {emissions:.2f} kg
    """)

# Compact button layout with better styling
st.markdown('''
    <style>
        div[data-testid="column"] {
            margin: 0px !important;
            padding: 0px 5px !important;
        }
        button[kind="secondary"] {
            width: 100% !important;
            margin: 2px 0 !important;
        }
        /* Floating chat always above all app content */
        #welink-float-chat, #welink-chatbox {
            position: fixed !important;
            z-index: 10050 !important;
            pointer-events: auto !important;
        }
        section.main, div.block-container, .stApp {
            overflow: visible !important;
        }
    </style>
''', unsafe_allow_html=True)

# Add navigation to other pages

# --- Ensure floating chat is called LAST ---

st.markdown(f"""
    <div style=\"margin-top: 2rem;\">
        <a href=\"#\" target=\"_self\" onclick=\"window.parent.document.querySelector('[data-testid=\\\"stSidebarNav\\\"]')?.click()\">
            ← {t.get('back_to_main_menu', 'Back to main menu')}
        </a>
    </div>
""", unsafe_allow_html=True)
