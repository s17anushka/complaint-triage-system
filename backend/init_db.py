# backend/init_db.py
from app.database import engine, Base
from app.models import User, OTPVerification, Complaint

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Database tables created successfully!")