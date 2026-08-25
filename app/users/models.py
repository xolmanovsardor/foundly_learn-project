from sqlalchemy import Column, Integer, String
from app.database import Base

class UserModel(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False, default="Azizbek") # Ism qo'shildi [_tY6yy]
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
