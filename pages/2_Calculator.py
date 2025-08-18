import streamlit as st
import os
from utils.page_config import set_page_config
from utils.i18n import get_translations
# Set page config with favicon
set_page_config("Calculator")

from utils.json_storage import save_carbon_footprint
from utils.data_processing import calculate_emissions
from datetime import datetime
from components.sidebar import show_sidebar
from components.ai_chat import floating_chat

t = get_translations()

# ... (rest of your page code)


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
    </style>
''', unsafe_allow_html=True)

# Show custom sidebar
show_sidebar()

# Check authentication
if not st.session_state.get('authenticated', False):
    st.switch_page("Home.py")

st.title("🌍 " + t['calculator'])

with st.form("calculator_form"):
    # SCOPE 1: Direct Emissions
    st.markdown(f'<h2 class="scope-header">🏭 {t.get("scope1", "SCOPE 1: Direct Emissions")}</h2>', unsafe_allow_html=True)

    # 1.A Stationary Combustion
    st.subheader("🔥 Stationary Combustion")
    ad_1a = st.number_input("Fuel consumption (TJ, Stationary)", min_value=0.0, value=0.0, key="stationary_fuel_consumption")
    ef_1a = st.number_input("CO₂ emission factor (kg CO₂/TJ, Stationary)", min_value=0.0, value=56100.0, key="stationary_ef")
    cc_1a = st.number_input("Carbon content (kg C/TJ, optional)", min_value=0.0, value=0.0, key="stationary_cc")
    use_cc_1a = st.checkbox("Use carbon content (Tier 2)", value=False, key="stationary_use_cc")

    # 1.B Mobile Combustion
    st.subheader("🚗 Mobile Combustion")
    fuel_road = st.number_input("Road Transport Fuel (TJ)", min_value=0.0, value=0.0, key="road_transport_fuel")
    ef_road = st.number_input("Road Transport EF (kg CO₂/TJ)", min_value=0.0, value=74100.0, key="road_transport_ef")
    fuel_rail = st.number_input("Railways Fuel (TJ)", min_value=0.0, value=0.0, key="railways_fuel")
    fuel_marine = st.number_input("Marine Navigation Fuel (TJ)", min_value=0.0, value=0.0, key="marine_fuel")
    ef_marine = st.number_input("Marine Navigation EF (kg CO₂/TJ)", min_value=0.0, value=77400.0, key="marine_ef")
    fuel_offroad = st.number_input("Off-road Vehicles Fuel (TJ)", min_value=0.0, value=0.0, key="offroad_fuel")
    ef_offroad = st.number_input("Off-road Vehicles EF (kg CO₂/TJ)", min_value=0.0, value=74100.0, key="offroad_ef")

    # 1.C Process Emissions
    st.subheader("🏭 Process Emissions (IPPU)")
    activity_proc = st.number_input("Process Activity Level (tonnes)", min_value=0.0, value=0.0, key="process_activity_level")
    ef_proc = st.number_input("Process Emission Factor (kg CO₂/tonne)", min_value=0.0, value=1000.0, key="process_ef")

    # 1.D Fugitive Emissions
    st.subheader("💨 Fugitive Emissions")
    ad_fug = st.number_input("Fugitive Activity Data (e.g., gas handled, tonnes)", min_value=0.0, value=0.0, key="fugitive_activity_data")
    ef_fug = st.number_input("Fugitive Emission Factor (kg CO₂/unit)", min_value=0.0, value=500.0, key="fugitive_ef")

    # Existing custom fields (retain)
    st.subheader("🔥 Custom Stationary Combustion (existing)")
    natural_gas = st.number_input(t.get("natural_gas", "Natural Gas (m³/year)"), min_value=0.0, value=0.0, key="custom_natural_gas")
    fuel_oil = st.number_input(t.get("fuel_oil", "Fuel Oil (liters/year)"), min_value=0.0, value=0.0, key="custom_fuel_oil")

    st.subheader("🚗 Custom Mobile Combustion (existing)")
    company_vehicles = st.number_input(t.get("company_vehicle_distance", "Company Vehicle Distance (km/year)"), min_value=0.0, value=0.0, key="custom_company_vehicle_distance")
    fleet_fuel = st.number_input(t.get("fleet_fuel_consumption", "Fleet Fuel Consumption (liters/year)"), min_value=0.0, value=0.0, key="custom_fleet_fuel_consumption")

    st.subheader("🏭 Custom Process Emissions (existing)")
    process_emissions = st.number_input(t.get("process_activity_data", "Process Activity Data (units/year)"), min_value=0.0, value=0.0, key="custom_process_activity_data")

    st.subheader("💨 Custom Fugitive Emissions (existing)")
    refrigerant_leakage = st.number_input(t.get("refrigerant_leakage", "Refrigerant Leakage (kg/year)"), min_value=0.0, value=0.0, key="custom_refrigerant_leakage")

    # SCOPE 2: Indirect Emissions from Purchased Energy
    st.markdown(f'<h2 class="scope-header">⚡ {t.get("scope2", "SCOPE 2: Indirect Emissions")}</h2>', unsafe_allow_html=True)
    ad_2 = st.number_input("Purchased Energy (kWh)", min_value=0.0, value=0.0, key="scope2_purchased_energy")
    ef_2 = st.number_input("Purchased Energy EF (kg CO₂e/kWh)", min_value=0.0, value=0.233, key="scope2_purchased_energy_ef")
    # Existing custom fields
    st.subheader("💻 Custom Purchased Electricity (existing)")
    electricity_kwh = st.number_input(t.get("electricity_usage", "Electricity Usage (kWh/year)"), min_value=0.0, value=0.0, key="custom_electricity_usage")
    renewable_percentage = st.slider(t.get("renewable_energy_percentage", "Renewable Energy Percentage"), 0, 100, 0, key="custom_renewable_percentage")
    st.subheader("🌡 Custom Purchased Heat/Steam (existing)")
    purchased_heat = st.number_input(t.get("heat_steam_usage", "Heat/Steam Usage (MWh/year)"), min_value=0.0, value=0.0, key="custom_heat_steam_usage")

    # SCOPE 3: All 15 Categories
    st.markdown(f'<h2 class="scope-header">🌐 {t.get("scope3", "SCOPE 3: Other Indirect Emissions")}</h2>', unsafe_allow_html=True)
    # 3.1 Purchased Goods & Services
    st.subheader("🛒 Purchased Goods & Services")
    spend_goods = st.number_input("Spend on Goods ($)", min_value=0.0, value=0.0, key="scope3_spend_goods")
    ef_spend_goods = st.number_input("EF for Spend (kg CO₂e/$)", min_value=0.0, value=0.43, key="scope3_ef_spend_goods")
    mass_goods = st.number_input("Mass of Goods Purchased (kg)", min_value=0.0, value=0.0, key="scope3_mass_goods")
    ef_mass_goods = st.number_input("EF for Mass (kg CO₂e/kg)", min_value=0.0, value=2.0, key="scope3_ef_mass_goods")
    # 3.2 Capital Goods
    st.subheader("🏗 Capital Goods")
    mass_capital = st.number_input("Mass of Capital Goods (kg)", min_value=0.0, value=0.0, key="scope3_mass_capital")
    ef_capital = st.number_input("EF for Capital Goods (kg CO₂e/kg)", min_value=0.0, value=2.0, key="scope3_ef_capital")
    # 3.3 Fuel & Energy-Related Activities
    st.subheader("⛽ Fuel & Energy-Related Activities")
    ad_wtt = st.number_input("Fuel/Energy Purchased (MJ)", min_value=0.0, value=0.0, key="scope3_fuel_energy_purchased")
    ef_wtt = st.number_input("Well-to-Tank EF (kg CO₂e/unit)", min_value=0.0, value=0.1, key="scope3_ef_wtt")
    # 3.4 Upstream Transportation & Distribution
    st.subheader("🚚 Upstream Transportation & Distribution")
    mass_upstream = st.number_input("Mass of Goods (kg, upstream)", min_value=0.0, value=0.0, key="scope3_mass_upstream")
    dist_upstream = st.number_input("Distance (km, upstream)", min_value=0.0, value=0.0, key="scope3_dist_upstream")
    ef_tonne_km_up = st.number_input("EF (kg CO₂e/tonne-km, upstream)", min_value=0.0, value=0.1, key="scope3_ef_tonne_km_up")
    # 3.5 Waste Generated in Operations
    st.subheader("🗑 Waste Generated in Operations")
    waste_mass = st.number_input("Waste Mass (kg)", min_value=0.0, value=0.0, key="scope3_waste_mass")
    doc = st.number_input("DOC (fraction)", min_value=0.0, max_value=1.0, value=0.2, key="scope3_doc")
    docf = st.number_input("DOCf (fraction)", min_value=0.0, max_value=1.0, value=0.5, key="scope3_docf")
    f = st.number_input("F (fraction)", min_value=0.0, max_value=1.0, value=0.5, key="scope3_f")
    r = st.number_input("R (fraction recovered)", min_value=0.0, max_value=1.0, value=0.0, key="scope3_r")
    ef_incineration = st.number_input("EF Incineration (kg CO₂/kg)", min_value=0.0, value=2.89, key="scope3_ef_incineration")
    # 3.6 Business Travel
    st.subheader("✈️ Business Travel (Scope 3)")
    dist_travel = st.number_input("Business Travel Distance (km)", min_value=0.0, value=0.0, key="scope3_business_travel_distance")
    ef_mode_travel = st.number_input("EF for Travel Mode (kg CO₂e/km)", min_value=0.0, value=0.2, key="scope3_ef_mode_travel")
    # 3.7 Employee Commuting
    st.subheader("🚌 Employee Commuting (Scope 3)")
    employees = st.number_input("Number of Employees", min_value=0, value=0, key="scope3_employees")
    trips_per_year = st.number_input("Trips per Year per Employee", min_value=0, value=220, key="scope3_trips_per_year")
    dist_avg_commute = st.number_input("Average Commute Distance (km)", min_value=0.0, value=0.0, key="scope3_avg_commute_distance")
    ef_mode_commute = st.number_input("EF for Commute Mode (kg CO₂e/km)", min_value=0.0, value=0.14, key="scope3_ef_mode_commute")
    # 3.8 Upstream Leased Assets
    st.subheader("🏢 Upstream Leased Assets")
    fuel_leased = st.number_input("Fuel Used by Leased Assets (TJ)", min_value=0.0, value=0.0, key="scope3_fuel_leased")
    ef_fuel_leased = st.number_input("EF for Leased Asset Fuel (kg CO₂/TJ)", min_value=0.0, value=56100.0, key="scope3_ef_fuel_leased")
    # 3.9 Downstream Transportation & Distribution
    st.subheader("🚛 Downstream Transportation & Distribution")
    mass_downstream = st.number_input("Mass of Goods (kg, downstream)", min_value=0.0, value=0.0, key="scope3_mass_downstream")
    dist_downstream = st.number_input("Distance (km, downstream)", min_value=0.0, value=0.0, key="scope3_dist_downstream")
    ef_tonne_km_down = st.number_input("EF (kg CO₂e/tonne-km, downstream)", min_value=0.0, value=0.1, key="scope3_ef_tonne_km_down")
    # 3.10 Processing of Sold Products
    st.subheader("🏭 Processing of Sold Products")
    mass_products = st.number_input("Mass of Sold Products (kg)", min_value=0.0, value=0.0, key="scope3_mass_sold_products")
    ef_processing = st.number_input("EF for Processing (kg CO₂/kg)", min_value=0.0, value=2.0, key="scope3_ef_processing")
    # 3.11 Use of Sold Products
    st.subheader("🔌 Use of Sold Products")
    energy_use_sold = st.number_input("Energy Use by Sold Products (kWh)", min_value=0.0, value=0.0, key="scope3_energy_use_sold")
    ef_energy_sold = st.number_input("EF for Sold Product Use (kg CO₂e/kWh)", min_value=0.0, value=0.233, key="scope3_ef_energy_sold")
    # 3.12 End-of-Life Treatment of Sold Products
    st.subheader("⚰️ End-of-Life Treatment of Sold Products")
    waste_products = st.number_input("Waste from Sold Products (kg)", min_value=0.0, value=0.0, key="scope3_waste_sold_products")
    ef_disposal = st.number_input("EF for Disposal (kg CO₂/kg)", min_value=0.0, value=2.0, key="scope3_ef_disposal")
    # 3.13 Downstream Leased Assets
    st.subheader("🏢 Downstream Leased Assets")
    fuel_downleased = st.number_input("Fuel Used by Downstream Leased Assets (TJ)", min_value=0.0, value=0.0, key="scope3_fuel_downleased")
    ef_fuel_downleased = st.number_input("EF for Downstream Leased Asset Fuel (kg CO₂/TJ)", min_value=0.0, value=56100.0, key="scope3_ef_fuel_downleased")
    # 3.14 Franchises
    st.subheader("🏪 Franchises")
    area_franchise = st.number_input("Franchise Area (m²)", min_value=0.0, value=0.0, key="scope3_franchise_area")
    ef_area = st.number_input("EF for Franchise Area (kg CO₂e/m²)", min_value=0.0, value=50.0, key="scope3_ef_franchise_area")
    # 3.15 Investments
    st.subheader("💼 Investments")
    investee_emissions = st.number_input("Investee Scope 1+2 Emissions (kg CO₂e)", min_value=0.0, value=0.0, key="scope3_investee_emissions")
    investment_value = st.number_input("Investment Value ($)", min_value=0.0, value=0.0, key="scope3_investment_value")
    ef_investment = st.number_input("EF for Investment (kg CO₂e/$)", min_value=0.0, value=0.2, key="scope3_ef_investment")

    # Existing custom Scope 3 fields (retain)
    st.subheader("✈️ Custom Business Travel (existing)")
    flight_miles = st.number_input(t.get("flight_distance", "Flight Distance (miles/year)"), min_value=0.0, value=0.0, key="custom_flight_distance")
    hotel_nights = st.number_input(t.get("hotel_nights", "Hotel Nights (nights/year)"), min_value=0.0, value=0.0, key="custom_hotel_nights")
    st.subheader("🚌 Custom Employee Commuting (existing)")
    num_employees = st.number_input(t.get("number_of_employees", "Number of Employees"), min_value=0, value=0, key="custom_num_employees")
    avg_commute = st.number_input(t.get("average_commute_distance", "Average Commute Distance (km/day)"), min_value=0.0, value=0.0, key="custom_avg_commute")
    work_days = st.number_input(t.get("work_days_per_year", "Work Days per Year"), min_value=0, value=220, key="custom_work_days")
    
    # Waste Management
    st.subheader("🗑 " + t.get("waste_management", "Waste Management"))
    waste_kg = st.number_input(t.get("waste_generated", "Waste Generated (kg/year)"), min_value=0.0, value=0.0, key="custom_waste_generated")
    recycling_percentage = st.slider(t.get("recycling_percentage", "Recycling Percentage"), 0, 100, 0, key="custom_recycling_percentage")
    
    # Purchased Goods
    st.subheader("💳 " + t.get("purchased_goods_services", "Purchased Goods & Services"))
    annual_spend = st.number_input(t.get("annual_procurement_spend", "Annual Procurement Spend ($)"), min_value=0.0, value=0.0, key="custom_annual_procurement_spend")
    
    submit = st.form_submit_button("📈 " + t.get("calculate", "Calculate Carbon Footprint"))
    
    if submit:
        try:
            # SCOPE 1 CALCULATIONS
            scope1_emissions = {}
            # 1.A Stationary Combustion
            if use_cc_1a and cc_1a > 0:
                e_1a = ad_1a * (cc_1a * (44/12))
            else:
                e_1a = ad_1a * ef_1a
            scope1_emissions['stationary_combustion'] = e_1a
            # 1.B Mobile Combustion
            scope1_emissions['road_transport'] = fuel_road * ef_road
            scope1_emissions['railways'] = fuel_rail * 4150 if fuel_rail > 0 else 0  # default EF for railways (kg CO2/TJ)
            scope1_emissions['marine_navigation'] = fuel_marine * ef_marine
            scope1_emissions['offroad_vehicles'] = fuel_offroad * ef_offroad
            # 1.C Process Emissions
            scope1_emissions['process_emissions'] = activity_proc * ef_proc
            # 1.D Fugitive Emissions
            scope1_emissions['fugitive_emissions'] = ad_fug * ef_fug
            # Existing custom fields
            scope1_emissions['custom_natural_gas'] = natural_gas * 2.1
            scope1_emissions['custom_fuel_oil'] = fuel_oil * 2.68
            scope1_emissions['custom_company_vehicles'] = company_vehicles * 0.14
            scope1_emissions['custom_fleet_fuel'] = fleet_fuel * 2.31
            scope1_emissions['custom_process'] = process_emissions * 1.0
            scope1_emissions['custom_fugitive'] = refrigerant_leakage * 1430
            scope1_total = sum(scope1_emissions.values())

            # SCOPE 2 CALCULATIONS
            scope2_emissions = {}
            scope2_emissions['purchased_energy'] = ad_2 * ef_2
            scope2_emissions['custom_electricity'] = electricity_kwh * 0.233 * (1 - renewable_percentage/100)
            scope2_emissions['custom_heat'] = purchased_heat * 270
            scope2_total = sum(scope2_emissions.values())

            # SCOPE 3 CALCULATIONS
            scope3_emissions = {}
            # 3.1 Purchased Goods & Services
            scope3_emissions['purchased_goods_spend'] = spend_goods * ef_spend_goods
            scope3_emissions['purchased_goods_mass'] = mass_goods * ef_mass_goods
            # 3.2 Capital Goods
            scope3_emissions['capital_goods'] = mass_capital * ef_capital
            # 3.3 Fuel & Energy-Related Activities
            scope3_emissions['fuel_energy_related'] = ad_wtt * ef_wtt
            # 3.4 Upstream Transportation & Distribution
            scope3_emissions['upstream_transport'] = (mass_upstream * dist_upstream) * ef_tonne_km_up
            # 3.5 Waste Generated in Operations
            scope3_emissions['waste_ch4'] = waste_mass * doc * docf * f * (16/12) * (1 - r)
            scope3_emissions['waste_co2_incineration'] = waste_mass * ef_incineration
            # 3.6 Business Travel
            scope3_emissions['business_travel'] = dist_travel * ef_mode_travel
            # 3.7 Employee Commuting
            scope3_emissions['employee_commuting'] = employees * trips_per_year * dist_avg_commute * ef_mode_commute
            # 3.8 Upstream Leased Assets
            scope3_emissions['upstream_leased_assets'] = fuel_leased * ef_fuel_leased
            # 3.9 Downstream Transportation & Distribution
            scope3_emissions['downstream_transport'] = (mass_downstream * dist_downstream) * ef_tonne_km_down
            # 3.10 Processing of Sold Products
            scope3_emissions['processing_sold_products'] = mass_products * ef_processing
            # 3.11 Use of Sold Products
            scope3_emissions['use_sold_products'] = energy_use_sold * ef_energy_sold
            # 3.12 End-of-Life Treatment
            scope3_emissions['end_of_life'] = waste_products * ef_disposal
            # 3.13 Downstream Leased Assets
            scope3_emissions['downstream_leased_assets'] = fuel_downleased * ef_fuel_downleased
            # 3.14 Franchises
            scope3_emissions['franchises'] = area_franchise * ef_area
            # 3.15 Investments
            scope3_emissions['investee_emissions'] = investee_emissions
            scope3_emissions['investment_value'] = investment_value * ef_investment
            # Existing custom fields
            scope3_emissions['custom_flight_miles'] = flight_miles * 0.200
            scope3_emissions['custom_hotel_nights'] = hotel_nights * 31.3
            scope3_emissions['custom_employee_commuting'] = num_employees * avg_commute * work_days * 0.14
            scope3_total = sum(scope3_emissions.values())

            # TOTAL EMISSIONS
            total_emissions = scope1_total + scope2_total + scope3_total

            # Save to JSON storage
            try:
                # Ensure the data directory exists
                data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
                os.makedirs(data_dir, exist_ok=True)
                
                # Save the footprint
                saved = save_carbon_footprint(
                    user_id=st.session_state.user_id,
                    scope1_emissions=scope1_total,
                    scope2_emissions=scope2_total,
                    scope3_emissions=scope3_total,
                    total_emissions=total_emissions,
                    emission_details={
                        'scope1': scope1_emissions,
                        'scope2': scope2_emissions,
                        'scope3': scope3_emissions
                    }
                )
                # Show results
                st.success("✅ Calculation saved successfully!")
                
                # Display results
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🏭 " + t.get("scope1_short", "Scope 1"), f"{scope1_total:.1f} kgCO₂e")
                with col2:
                    st.metric("⚡ " + t.get("scope2_short", "Scope 2"), f"{scope2_total:.1f} kgCO₂e")
                with col3:
                    st.metric("🌐 " + t.get("scope3_short", "Scope 3"), f"{scope3_total:.1f} kgCO₂e")
                st.metric("🌍 " + t.get("total_carbon_footprint", "Total Carbon Footprint"), 
                        f"{total_emissions:.1f} kgCO₂e",
                        delta=f"{total_emissions/1000:.2f} Metric Tons")
                
            except Exception as e:
                st.error(f"Error saving calculation: {str(e)}")
                st.error("Please check if the data directory has write permissions.")
                
                # Verify the data was saved
                from utils.json_storage import get_user_footprints
                footprints = get_user_footprints(st.session_state.user_id)
                print(f"Found {len(footprints)} footprints for user {st.session_state.user_id}")
                
            except Exception as e:
                print(f"Error saving footprint: {str(e)}")
                st.error(f"Error saving your data: {str(e)}")

            # Success message is now shown in the try block
        except Exception as e:
            st.error(f"Error calculating carbon footprint: {str(e)}")

# Add a button to view detailed history (must be outside the form)
if st.button("📈 " + t.get("view_detailed_history", "View Detailed History")):
    st.switch_page("pages/3_History.py")
