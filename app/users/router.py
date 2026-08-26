import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.listings.models import ListingModel
from app.users.models import UserModel
from app.users.repository import UserRepository
from app.users.schemas import (
    ProfileResponseSchema,
    TokenSchema,
    UserLoginSchema,
    UserRegisterSchema,
    UserResponseSchema,
)
from app.users.service import UserService


router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post(
    "/register",
    response_model=UserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserRegisterSchema,
    db: Session = Depends(get_db),
) -> UserModel:
    user_service = UserService(UserRepository(db))
    return user_service.register_user(user_data)


@router.post("/login", response_model=TokenSchema)
def login_user(
    login_data: UserLoginSchema,
    db: Session = Depends(get_db),
) -> TokenSchema:
    user_service = UserService(UserRepository(db))
    return user_service.login_user(login_data)


@router.get("/me", response_model=ProfileResponseSchema)
def get_my_profile(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> ProfileResponseSchema:
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        user_id = int(payload["sub"])
    except (jwt.PyJWTError, KeyError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token yaroqsiz",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Foydalanuvchi topilmadi",
        )

    total = db.query(ListingModel).filter(ListingModel.user_id == user.id).count()
    active = db.query(ListingModel).filter(
        ListingModel.user_id == user.id,
        ListingModel.status == "ACTIVE",
    ).count()
    received = db.query(ListingModel).filter(
        ListingModel.user_id == user.id,
        ListingModel.status == "CLAIMED",
    ).count()

    return ProfileResponseSchema(
        id=user.id,
        first_name=user.first_name,
        email=user.email,
        total_listings=total,
        active_listings=active,
        received_listings=received,
    )
