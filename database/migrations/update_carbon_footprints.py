from sqlalchemy import create_engine, text
from database import DATABASE_URL

def migrate():
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Drop existing table and sequence
        conn.execute(text("DROP TABLE IF EXISTS carbon_footprints_new"))
        conn.execute(text("DROP TABLE IF EXISTS carbon_footprints CASCADE"))
        conn.execute(text("DROP SEQUENCE IF EXISTS carbon_footprints_id_seq"))
        
        # Create sequence
        conn.execute(text("""
            CREATE SEQUENCE carbon_footprints_id_seq
            START WITH 1
            INCREMENT BY 1
            NO MINVALUE
            NO MAXVALUE
            CACHE 1
        """))
        
        # Create new table
        conn.execute(text("""
            CREATE TABLE carbon_footprints (
                id INTEGER DEFAULT nextval('carbon_footprints_id_seq') PRIMARY KEY,
                user_id INTEGER NOT NULL REFERENCES users(id),
                created_at FLOAT NOT NULL,
                scope1_emissions FLOAT NOT NULL,
                scope2_emissions FLOAT NOT NULL,
                scope3_emissions FLOAT NOT NULL,
                total_emissions FLOAT NOT NULL,
                emission_details JSONB NOT NULL
            )
        """))
        
        # Set the sequence ownership
        conn.execute(text("""
            ALTER SEQUENCE carbon_footprints_id_seq
            OWNED BY carbon_footprints.id
        """))
        
        conn.commit()

if __name__ == "__main__":
    migrate()
