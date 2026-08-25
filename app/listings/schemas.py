from pydantic import BaseModel, Field
from typing import Optional

# Yangi e'lon qo'shish oynasi uchun ma'lumotlar shakli (Rasmga mos holatda) [KUCKkU]
class ListingCreateSchema(BaseModel):
    type: str = Field(..., description="Listing Type: Found yoki Lost") # Listing Type [KUCKkU]
    title: str = Field(..., min_length=2, max_length=100)              # Title (2-100 belgi) [KUCKkU]
    description: Optional[str] = Field(None, max_length=300)          # Description (max 300 belgi) [KUCKkU]
    date_found: str = Field(..., description="Date Found: Sana")       # Date Found [KUCKkU]
    image_url: Optional[str] = Field(None, description="Add Photo linki") # Add Photo [KUCKkU]

# Bazadan ma'lumot qaytayotganda chiqadigan shakl [oxdFQS]
class ListingResponseSchema(BaseModel):
    id: int
    type: str
    title: str
    description: Optional[str] = None
    date_found: str
    image_url: Optional[str] = None
    status: str
    user_id: int

    class Config:
        from_attributes = True
