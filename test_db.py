from database import engine
from database.models import Base
from sqlalchemy import text

def reset_database():
    try:
        # Test raw connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("✅ Existing tables dropped successfully!")
            
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Tables recreated successfully!")
        
        return True
    except Exception as e:
        print("❌ Database operation failed!")
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    reset_database()
