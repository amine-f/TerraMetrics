from datetime import datetime
import pandas as pd

def process_footprint_data(footprints):
    """Convert footprint data to a pandas DataFrame."""
    if not footprints:
        return None
        
    data = [{
        'Date': datetime.fromtimestamp(f.created_at).strftime('%Y-%m-%d %H:%M'),
        'Transportation': f.transportation_emissions,
        'Electricity': f.electricity_emissions,
        'Diet': f.diet_emissions,
        'Waste': f.waste_emissions,
        'Total': f.total_emissions
    } for f in footprints]
    
    return pd.DataFrame(data)

def calculate_emissions(transportation_data, electricity_data, diet_data, waste_data):
    """Calculate emissions for each category."""
    # Emission factors
    TRANSPORT_FACTORS = {
        'car_miles': 0.404,     # kg CO2 per mile
        'public_miles': 0.14,    # kg CO2 per mile
        'flight_miles': 0.257    # kg CO2 per mile
    }
    
    ELECTRICITY_FACTORS = {
        'kwh': 0.433  # kg CO2 per kWh
    }
    
    DIET_FACTORS = {
        'meat_servings': 3.3,    # kg CO2 per serving
        'dairy_servings': 1.9     # kg CO2 per serving
    }
    
    WASTE_FACTORS = {
        'landfill_kg': 2.89  # kg CO2 per kg waste
    }
    
    # Transportation emissions calculation
    transport_emissions = sum(
        miles * TRANSPORT_FACTORS[key]
        for key, miles in transportation_data.items()
    )
    
    # Electricity emissions calculation
    electricity_emissions = sum(
        kwh * ELECTRICITY_FACTORS[key]
        for key, kwh in electricity_data.items()
    )
    
    # Diet emissions calculation
    diet_emissions = sum(
        servings * DIET_FACTORS[key]
        for key, servings in diet_data.items()
    )
    
    # Waste emissions calculation
    waste_emissions = sum(
        kg * WASTE_FACTORS[key]
        for key, kg in waste_data.items()
    )
    
    # Convert from kg to tonnes
    transport_emissions = round(transport_emissions / 1000, 2)
    electricity_emissions = round(electricity_emissions / 1000, 2)
    diet_emissions = round(diet_emissions / 1000, 2)
    waste_emissions = round(waste_emissions / 1000, 2)
    
    total_emissions = round(
        transport_emissions + electricity_emissions + diet_emissions + waste_emissions,
        2
    )
    
    return {
        'Transportation': transport_emissions,
        'Electricity': electricity_emissions,
        'Diet': diet_emissions,
        'Waste': waste_emissions,
        'Total': total_emissions
    }
