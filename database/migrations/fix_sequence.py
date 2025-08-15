from sqlalchemy import create_engine, text
from database import DATABASE_URL

def fix_sequence():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Get the current maximum id
        result = conn.execute(text("SELECT MAX(id) FROM carbon_footprints"))
        max_id = result.scalar() or 0
        
        # Reset the sequence to start from the next available id
        conn.execute(text(f"""
            SELECT setval('carbon_footprints_id_seq', {max_id}, true)
        """))
        
        conn.commit()

if __name__ == "__main__":
    fix_sequence()
