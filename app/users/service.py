import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status
from passlib.context import CryptContext

from app.core.config import settings
from app.users.repository import UserRepository
from app.users.schemas import UserRegisterSchema, UserLoginSchema, TokenSchema

# Parollarni xavfsiz shifrlash (hash) sozlamasi
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    # MANA SHU FUNKSIYA SIZDA QOLIB KETGAN EDI (Hozirgi xatoni tuzatuvchi qism):
    def __init__(self, repository: UserRepository):
        self.repository = repository

    # 1. Ro'yxatdan o'tish (Register)
    def register_user(self, user_data: UserRegisterSchema):
        existing_user = self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Bu email manzili allaqachon ro'yxatdan o'tgan!"
            )
        hashed_password = pwd_context.hash(user_data.password)
        return self.repository.create_user(email=user_data.email, hashed_password=hashed_password)

    # 2. Tizimga kirish (Login)
    def login_user(self, login_data: UserLoginSchema) -> TokenSchema:
        user = self.repository.get_user_by_email(login_data.email)
        
        # Parol yoki email xato bo'lsa 401 xatosini qaytaramiz
        if not user or not pwd_context.verify(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email yoki parol noto'g'ri!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Token muddati (1 kunga amal qiladi)
        expire = datetime.now(timezone.utc) + timedelta(days=1)
        payload = {"email": user.email, "exp": expire}
        
        # .env ichidagi kalit orqali token shifrlanadi
        token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        
        return TokenSchema(access_token=token)
