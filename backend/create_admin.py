# backend/create_admin.py

import os
from app.database import SessionLocal
from app.models import User
from app.auth import hash_password

db = SessionLocal()


EMAIL = os.getenv("ADMIN_EMAIL")
PASSWORD = os.getenv("ADMIN_PASSWORD")

if not EMAIL or not PASSWORD:
    raise Exception(
        "❌ ADMIN_EMAIL or ADMIN_PASSWORD not set.\n"
        "Set them in .env (local) or Environment Variables (cloud)."
    )

print(f"\n{'='*50}")
print(f"Creating / Updating Admin User")
print(f"{'='*50}")

existing = db.query(User).filter(User.email == EMAIL).first()

if existing:
    print(f"\n User already exists!")
    print(f"   Email: {existing.email}")
    print(f"   Current Role: {existing.role}")

    existing.password_hash = hash_password(PASSWORD)
    existing.role = "admin"
    db.commit()

    print(f"\n✅ User updated successfully!")
    print(f"   Email: {existing.email}")
    print(f"   Role: {existing.role}")
    print(f"   Password: Updated")

else:
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
print(f"🔑 Admin setup completed")
print(f"{'='*50}\n")

db.close()
