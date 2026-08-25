from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt

from app.database import get_db
from app.core.config import settings
from app.users.schemas import ProfileResponseSchema
from app.users.models import UserModel
from app.listings.models import ListingModel  # E'lonlarni hisoblash uchun

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@router.get("/me", response_model=ProfileResponseSchema)
def get_my_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token xato")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token yaroqsiz")

    # 1. Foydalanuvchini topamiz
    user = db.query(UserModel).filter(UserModel.id == int(user_id)).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Foydalanuvchi topilmadi")

    # 2. Rasmda so'ralgan barcha statistikani hisoblaymiz [_tY6yy]:
    total = db.query(ListingModel).filter(ListingModel.user_id == user.id).count()
    active = db.query(ListingModel).filter(ListingModel.user_id == user.id, ListingModel.status == "ACTIVE").count()
    received = db.query(ListingModel).filter(ListingModel.user_id == user.id, ListingModel.status == "CLAIMED").count()

    # 3. Yakuniy javobni qaytaramiz
    return ProfileResponseSchema(
        id=user.id,
        first_name=user.first_name,
        email=user.email,
        total_listings=total,
        active_listings=active,
        received_listings=received
    )
