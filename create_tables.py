from database.models import Base
from database import engine

# Create all tables in the database
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")