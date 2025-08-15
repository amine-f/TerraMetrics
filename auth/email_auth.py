from database import models, SessionLocal
from passlib.context import CryptContext
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# User registration
def register_user(email: str, password: str):
    try:
        db = next(get_db())
        # Check if user already exists
        existing_user = db.query(models.User).filter(models.User.email == email).first()
        if existing_user:
            print(f"User with email {email} already exists")
            return "exists"
            
        hashed_password = pwd_context.hash(password)
        # Ensure the fields match the User model
        new_user = models.User(email=email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        send_verification_email(email)
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False

# User login
def login_user(email: str, password: str):
    try:
        db = next(get_db())
        user = db.query(models.User).filter(models.User.email == email).first()
        if user and pwd_context.verify(password, user.password):
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