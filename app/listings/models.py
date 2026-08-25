from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base

class ListingModel(Base):
    __tablename__ = "listings"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)          # Listing Type [KUCKkU]
    title = Column(String, index=True, nullable=False) # Title [KUCKkU]
    description = Column(Text, nullable=True)       # Description [KUCKkU]
    date_found = Column(String, nullable=False)     # Date Found [KUCKkU]
    image_url = Column(String, nullable=True)       # Add Photo [KUCKkU]
    
    # Shart bo'yicha: status doim ACTIVE bo'lib yaratiladi [oxdFQS, KUCKkU]
    status = Column(String, nullable=False, default="ACTIVE") 
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
