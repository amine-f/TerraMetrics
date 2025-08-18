import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from passlib.context import CryptContext

# Import our JSON storage
from utils.json_storage import create_user, verify_user, get_user_by_email

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User registration
def register_user(email: str, password: str):
    try:
        # Check if user already exists
        if get_user_by_email(email):
            print(f"User with email {email} already exists")
            return "exists"
            
        # Hash the password
        hashed_password = pwd_context.hash(password)
        
        # Create new user in JSON storage
        new_user = create_user(email, hashed_password)
        
        # Skip email verification for now
        print(f"User {email} registered successfully (email verification skipped)")
        return new_user
        
        # Uncomment to enable email verification
        # try:
        #     send_verification_email(email)
        #     return new_user
        # except Exception as e:
        #     print(f"Warning: Could not send verification email: {e}")
        #     return new_user  # Still return user even if email fails
            
    except Exception as e:
        print(f"Error during registration: {e}")
        return None

# User login
def login_user(email: str, password: str):
    try:
        # Get user from JSON storage
        user = get_user_by_email(email)
        if user is None:
            print(f"No user found with email: {email}")
            return None
            
        # Verify password
        if not pwd_context.verify(password, user["password"]):
            print(f"Invalid password for user: {email}")
            return None
            
        print(f"User {email} logged in successfully")
        return user
        
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