import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database import get_db
from app.users.models import UserModel


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
	token: str = Depends(oauth2_scheme),
	db: Session = Depends(get_db),
) -> UserModel:
	try:
		payload = jwt.decode(
			token,
			settings.JWT_SECRET_KEY,
			algorithms=[settings.JWT_ALGORITHM],
		)
		user_email = payload["email"]
	except (jwt.PyJWTError, KeyError, TypeError, ValueError):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Token yaroqsiz",
			headers={"WWW-Authenticate": "Bearer"},
		)

	user = db.query(UserModel).filter(UserModel.email == user_email).first()
	if user is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Foydalanuvchi topilmadi",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return user
