from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..auth import verify_password, create_access_token, get_current_user
from ..schemas import AdminLoginRequest

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/admin/login")
def admin_login(data: AdminLoginRequest, db: Session = Depends(get_db)):
    """
    Admin login WITHOUT OTP
    """

    admin = db.query(User).filter(
        User.email == data.email,
        User.role == "admin"
    ).first()

    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")

    if not verify_password(data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({
        "sub": admin.email,
        "role": admin.role,
        "user_id": admin.id
    })

    return {
        "access_token": token,
        "token_type": "bearer",
        "email": admin.email,
        "role": admin.role
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "email": current_user.get("sub"),
        "role": current_user.get("role"),
        "user_id": current_user.get("user_id")
    }
