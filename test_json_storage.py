"""Test script to verify JSON storage functionality."""
import sys
import os
import json
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent))

from utils.json_storage import (
    create_user, 
    verify_user, 
    save_carbon_footprint, 
    get_user_footprints,
    load_data
)

def test_json_storage():
    print("=== Testing JSON Storage ===")
    
    # Test data
    test_email = "test@example.com"
    test_password = "test123"
    
    # 1. Test creating a user
    print("\n1. Testing user creation...")
    user = create_user(test_email, test_password)
    print(f"Created user: {user}")
    
    # 2. Test verifying the user
    print("\n2. Testing user verification...")
    verified_user = verify_user(test_email, test_password)
    print(f"Verified user: {verified_user is not None}")
    
    if not verified_user:
        print("User verification failed!")
        return
    
    # 3. Test saving a carbon footprint
    print("\n3. Testing carbon footprint save...")
    footprint = save_carbon_footprint(
        user_id=verified_user["id"],
        scope1_emissions=100.5,
        scope2_emissions=50.2,
        scope3_emissions=200.1,
        total_emissions=350.8,
        emission_details={
            'scope1': {'fuel_combustion': 100.5},
            'scope2': {'electricity': 50.2},
            'scope3': {'travel': 100.0, 'waste': 100.1}
        }
    )
    print(f"Saved footprint: {footprint}")
    
    # 4. Test retrieving user footprints
    print("\n4. Testing footprint retrieval...")
    footprints = get_user_footprints(verified_user["id"])
    print(f"Found {len(footprints)} footprints for user:")
    for i, fp in enumerate(footprints, 1):
        print(f"  {i}. ID: {fp['id']}, Total: {fp['total_emissions']} kgCO2e")
    
    # 5. Show raw data
    print("\n5. Raw data file content:")
    data = load_data()
    print(json.dumps(data, indent=2))
    
    print("\n=== Test Completed Successfully ===")

if __name__ == "__main__":
    # Make sure we're using the test data file
    os.environ["TEST_MODE"] = "1"
    test_json_storage()
