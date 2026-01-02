# backend/create_admin.py
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password  # ✅ Correct import

db = SessionLocal()

EMAIL = "m9anushka@gmail.com"
PASSWORD = "admin123"  # ⚠️ Change this to your actual password

print(f"\n{'='*50}")
print(f"Creating/Updating Admin User")
print(f"{'='*50}")

# Check if user exists
existing = db.query(User).filter(User.email == EMAIL).first()

if existing:
    print(f"\n⚠️  User already exists!")
    print(f"   Email: {existing.email}")
    print(f"   Current Role: {existing.role}")
    
    # Update password and ensure role is admin
    existing.password_hash = hash_password(PASSWORD)
    existing.role = "admin"
    db.commit()
    
    print(f"\n✅ User updated successfully!")
    print(f"   Email: {existing.email}")
    print(f"   Role: {existing.role}")
    print(f"   Password: Updated")
    
else:
    # Create new admin
    print(f"\n📝 Creating new admin user...")
    
    admin = User(
        email=EMAIL,
        password_hash=hash_password(PASSWORD),
        role="admin"
    )
    
    db.add(admin)
    db.commit()
    db.refresh(admin)
    
    print(f"\n✅ Admin created successfully!")
    print(f"   ID: {admin.id}")
    print(f"   Email: {admin.email}")
    print(f"   Role: {admin.role}")

print(f"\n{'='*50}")
print(f"🔑 Login Credentials:")
print(f"{'='*50}")
print(f"   Email: {EMAIL}")
print(f"   Password: {PASSWORD}")
print(f"{'='*50}\n")

db.close()