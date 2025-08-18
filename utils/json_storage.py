"""
JSON-based storage system to replace SQLite database.
Stores all data in a single JSON file in the user's home directory.
"""
import os
import json
from datetime import datetime
from pathlib import Path

# Get the absolute path to the data directory
BASE_DIR = Path(__file__).parent.parent  # Go up two levels to the project root
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "carbon_data.json"

# Create data directory if it doesn't exist
os.makedirs(DATA_DIR, exist_ok=True, mode=0o777)

# Initialize data structure if file doesn't exist
if not DATA_FILE.exists():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump({"users": [], "carbon_footprints": []}, f, indent=2)
        # Ensure the file has the right permissions
        os.chmod(DATA_FILE, 0o666)
        print(f"Initialized data file at: {DATA_FILE}")
    except Exception as e:
        print(f"Error initializing data file: {e}")
        print(f"Data file path: {DATA_FILE}")
        print(f"Directory exists: {os.path.exists(DATA_DIR)}")
        print(f"Directory writable: {os.access(DATA_DIR, os.W_OK)}")
        raise

def load_data():
    """Load all data from the JSON file with error handling and validation."""
    try:
        # If file doesn't exist, initialize it
        if not DATA_FILE.exists():
            reset_data()
            return {"users": [], "carbon_footprints": []}
            
        # Try to read and parse the file
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            
        # Validate the data structure
        if not isinstance(data, dict) or "users" not in data or "carbon_footprints" not in data:
            print("Invalid data structure, resetting...")
            reset_data()
            return {"users": [], "carbon_footprints": []}
            
        return data
        
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        # Try to recover by resetting the file
        reset_data()
        return {"users": [], "carbon_footprints": []}
        
    except Exception as e:
        print(f"Unexpected error loading data: {e}")
        reset_data()
        return {"users": [], "carbon_footprints": []}

def save_data(data):
    """Save data to the JSON file with error handling and backup."""
    try:
        # Create a backup of the current data
        backup_file = f"{DATA_FILE}.bak"
        if DATA_FILE.exists():
            import shutil
            shutil.copy2(DATA_FILE, backup_file)
        
        # Write new data
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
            
        # Verify the data was written correctly
        with open(DATA_FILE, 'r') as f:
            loaded = json.load(f)
            if loaded != data:
                raise ValueError("Data verification failed after write")
                
    except Exception as e:
        print(f"Error saving data: {e}")
        # Try to restore from backup if available
        if 'backup_file' in locals() and os.path.exists(backup_file):
            try:
                shutil.copy2(backup_file, DATA_FILE)
                print("Restored data from backup")
            except Exception as restore_error:
                print(f"Failed to restore from backup: {restore_error}")
        raise

def reset_data():
    """Reset the data file to initial state."""
    with open(DATA_FILE, 'w') as f:
        json.dump({"users": [], "carbon_footprints": []}, f, indent=2)

# User operations
def get_user_by_email(email):
    """Get a user by email."""
    data = load_data()
    for user in data["users"]:
        if user["email"] == email:
            return user
    return None

def create_user(email, password):
    """Create a new user."""
    data = load_data()
    
    # Check if user already exists
    if get_user_by_email(email):
        raise ValueError("User with this email already exists")
    
    # Create new user
    user_id = len(data["users"]) + 1
    new_user = {
        "id": user_id,
        "email": email,
        "password": password,  # In a real app, this should be hashed
        "created_at": datetime.utcnow().timestamp()
    }
    
    data["users"].append(new_user)
    save_data(data)
    return new_user

def verify_user(email, password):
    """Verify user credentials."""
    user = get_user_by_email(email)
    if user and user["password"] == password:  # In a real app, use proper password hashing
        return user
    return None

# Carbon footprint operations
def save_carbon_footprint(user_id, scope1_emissions, scope2_emissions, scope3_emissions, total_emissions, emission_details):
    """Save a new carbon footprint record."""
    try:
        # Ensure data directory exists
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # Initialize data file if it doesn't exist
        if not DATA_FILE.exists():
            with open(DATA_FILE, 'w') as f:
                json.dump({"users": [], "carbon_footprints": []}, f)
        
        # Load existing data
        data = load_data()
        
        # Create new record
        new_record = {
            "id": len(data["carbon_footprints"]) + 1,
            "user_id": user_id,
            "created_at": datetime.utcnow().timestamp(),
            "scope1_emissions": scope1_emissions,
            "scope2_emissions": scope2_emissions,
            "scope3_emissions": scope3_emissions,
            "total_emissions": total_emissions,
            "emission_details": emission_details
        }
        
        # Add new record and save
        data["carbon_footprints"].append(new_record)
        save_data(data)
        return new_record
    except Exception as e:
        print(f"Error in save_carbon_footprint: {str(e)}")
        raise

def get_user_footprints(user_id):
    """Get all carbon footprints for a user."""
    try:
        # Ensure data directory and file exist
        os.makedirs(DATA_DIR, exist_ok=True)
        if not DATA_FILE.exists():
            with open(DATA_FILE, 'w') as f:
                json.dump({"users": [], "carbon_footprints": []}, f)
        
        # Load data and filter by user_id
        data = load_data()
        if not isinstance(data, dict) or "carbon_footprints" not in data:
            return []
            
        return [f for f in data["carbon_footprints"] if f.get("user_id") == user_id]
    except Exception as e:
        print(f"Error in get_user_footprints: {str(e)}")
        return []
