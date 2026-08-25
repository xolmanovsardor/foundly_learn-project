from fastapi import APIRouter, Depends, Query, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from typing import List

from app.database import get_db
from app.core.config import settings
from app.listings.schemas import ListingResponseSchema, ListingCreateSchema
from app.listings.repository import ListingRepository
from app.listings.service import ListingService

router = APIRouter(prefix="/listings", tags=["Listings"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# PUBLISH LISTING (PUSH TUGMASI LOGIKASI) [KUCKkU]
@router.post("", response_model=ListingResponseSchema, status_code=status.HTTP_201_CREATED)
def create_listing(
    listing_in: ListingCreateSchema, 
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
):
    try:
        # user_id request'dan olinmaydi, token'dan olinadi! [KUCKkU]
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token xato")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token yaroqsiz")

    repository = ListingRepository(db)
    service = ListingService(repository)
    return service.create_listing(listing_in, user_id=int(user_id))

@router.get("", response_model=List[ListingResponseSchema])
def get_all_listings(
    search: str = Query(None),
    type: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1),
    db: Session = Depends(get_db)
):
    repository = ListingRepository(db)
    service = ListingService(repository)
    return service.get_listings(search=search, type=type, page=page, page_size=page_size)

@router.get("/{id}", response_model=ListingResponseSchema)
def get_listing(id: int, db: Session = Depends(get_db)):
    repository = ListingRepository(db)
    service = ListingService(repository)
    return service.get_single_listing(listing_id=id)

@router.post("/{id}/claim", response_model=ListingResponseSchema)
def claim_item(id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token xato")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token muddati o'tgan")

    repository = ListingRepository(db)
    service = ListingService(repository)
    return service.claim_listing(listing_id=id)
