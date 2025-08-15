import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# App settings
APP_NAME = "Terrametrics"
APP_LAYOUT = "wide"

# Database settings
DATABASE_URL = os.getenv('DATABASE_URL')

# Email settings
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
