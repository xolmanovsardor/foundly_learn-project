from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.listings.schemas import ListingResponseSchema, ListingCreateSchema
from app.listings.repository import ListingRepository
from app.listings.service import ListingService
from app.users.dependencies import get_current_user
from app.users.models import UserModel

router = APIRouter(prefix="/listings", tags=["Listings"])
my_listings_router = APIRouter(prefix="/me", tags=["Listings"])

# PUBLISH LISTING (PUSH TUGMASI LOGIKASI) [KUCKkU]
@router.post("", response_model=ListingResponseSchema, status_code=status.HTTP_201_CREATED)
def create_listing(
    listing_in: ListingCreateSchema, 
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    repository = ListingRepository(db)
    service = ListingService(repository)
    return service.create_listing(listing_in, user_id=current_user.id)

@router.get("", response_model=List[ListingResponseSchema])
def get_all_listings(
    search: str = Query(None),
    type: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
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
def claim_item(id: int, current_user: UserModel = Depends(get_current_user), db: Session = Depends(get_db)):
    repository = ListingRepository(db)
    service = ListingService(repository)
    return service.claim_listing(listing_id=id)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(
    id: int,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ListingService(ListingRepository(db))
    service.delete_listing(listing_id=id, user_id=current_user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@my_listings_router.get("/listings", response_model=List[ListingResponseSchema])
def get_my_listings(
    search: str = Query(None),
    type: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = ListingService(ListingRepository(db))
    return service.get_user_listings(
        user_email=current_user.email,
        search=search,
        type=type,
        page=page,
        page_size=page_size,
    )
