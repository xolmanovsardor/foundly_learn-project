from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.listings.models import ListingModel
from app.users.models import UserModel
from app.users.dependencies import get_current_user
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
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ProfileResponseSchema:
    total = db.query(ListingModel).filter(ListingModel.user_id == current_user.id).count()
    active = db.query(ListingModel).filter(
        ListingModel.user_id == current_user.id,
        ListingModel.status == "ACTIVE",
    ).count()
    received = db.query(ListingModel).filter(
        ListingModel.user_id == current_user.id,
        ListingModel.status == "CLAIMED",
    ).count()

    return ProfileResponseSchema(
        id=current_user.id,
        first_name=current_user.first_name,
        email=current_user.email,
        total_listings=total,
        active_listings=active,
        received_listings=received,
    )
