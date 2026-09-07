from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import (
    verify_password, get_password_hash, create_access_token, get_current_active_user
)
from app.models.models import User, UserProfile
from .schemas import LoginRequest, RegisterRequest, ForgotPasswordRequest, AuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=AuthResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect official email or password"
        )
    
    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    onboarding_done = user.profile.onboarding_completed if user.profile else False
    
    return AuthResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        onboarding_completed=onboarding_done
    )

@router.post("/register", response_model=AuthResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == req.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this official email already exists"
        )
    
    user = User(
        email=req.email,
        password_hash=get_password_hash(req.password),
        full_name=req.full_name,
        role=req.role if req.role in ["learner", "admin"] else "learner"
    )
    db.add(user)
    db.flush()

    # Create empty profile requiring onboarding
    profile = UserProfile(
        user_id=user.id,
        onboarding_completed=False
    )
    db.add(profile)
    db.commit()

    token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return AuthResponse(
        access_token=token,
        user_id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        onboarding_completed=False
    )

@router.post("/forgot-password")
def forgot_password(req: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == req.email).first()
    # Always return success message for security/privacy
    return {
        "message": f"If an account exists for {req.email}, password reset instructions have been dispatched to your official mail."
    }

@router.get("/me", response_model=AuthResponse)
def get_me(current_user: User = Depends(get_current_active_user)):
    onboarding_done = current_user.profile.onboarding_completed if current_user.profile else False
    token = create_access_token(data={"sub": str(current_user.id), "role": current_user.role})
    return AuthResponse(
        access_token=token,
        user_id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        onboarding_completed=onboarding_done
    )
