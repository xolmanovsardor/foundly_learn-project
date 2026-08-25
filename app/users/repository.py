from sqlalchemy.orm import Session
from app.users.models import UserModel

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # Email bo'yicha foydalanuvchini bazadan qidirish
    def get_user_by_email(self, email: str) -> UserModel | None:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    # Yangi foydalanuvchini bazaga qo'shish
    def create_user(self, email: str, hashed_password: str, first_name: str = "Azizbek") -> UserModel:
        db_user = UserModel(email=email, hashed_password=hashed_password, first_name=first_name)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
