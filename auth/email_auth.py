import json
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Path to the user data file
USER_DATA_FILE = 'users.json'

# Function to read user data from the file
def read_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return []
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

# Function to write user data to the file
def write_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# User registration
def register_user(email: str, password: str):
    try:
        users = read_user_data()
        # Check if user already exists
        if any(user['email'] == email for user in users):
            print(f"User with email {email} already exists")
            return "exists"

        hashed_password = pwd_context.hash(password)
        new_user = {'email': email, 'password': hashed_password}
        users.append(new_user)
        write_user_data(users)
        send_verification_email(email)
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False

# User login
def login_user(email: str, password: str):
    try:
        users = read_user_data()
        user = next((user for user in users if user['email'] == email), None)
        if user and pwd_context.verify(password, user['password']):
            return user
        return None
    except Exception as e:
        print(f"Error during login: {e}")
        return None

# Send verification email
def send_verification_email(email: str):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    receiver_email = email

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Email Verification"

    body = "Please verify your email address."
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("Verification email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")