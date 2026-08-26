from fastapi import HTTPException, status
from app.listings.repository import ListingRepository
from app.listings.schemas import ListingCreateSchema

class ListingService:
    def __init__(self, repository: ListingRepository):
        self.repository = repository

    # 1. Barcha e'lonlarni olish
    def get_listings(self, search: str = None, type: str = None, page: int = 1, page_size: int = 20):
        return self.repository.get_all_listings(search=search, type=type, page=page, page_size=page_size)

    def get_user_listings(self, user_email: str, search: str = None, type: str = None, page: int = 1, page_size: int = 20):
        return self.repository.get_user_listings(
            user_email=user_email,
            search=search,
            type=type,
            page=page,
            page_size=page_size,
        )

    # 2. Yangi e'lon yaratish (Hozirgi xatoni tuzatgan qism)
    def create_listing(self, listing_data: ListingCreateSchema, user_id: int):
        return self.repository.create_new_listing(listing_data, user_id)

    # 3. Bitta e'lonni ID bo'yicha olish (404 xatoligi tekshiruvi bilan)
    def get_single_listing(self, listing_id: int):
        listing = self.repository.get_listing_by_id(listing_id)
        if not listing:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="E'lon topilmadi!"
            )
        return listing

    # 4. E'lonni band qilish / claim (409 xatoligi tekshiruvi bilan)
    def claim_listing(self, listing_id: int):
        listing = self.get_single_listing(listing_id) # Oldin 404 likka tekshiradi
        
        if listing.status == "CLAIMED":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Bu e'lon allaqachon claim qilingan!"
            )
            
        return self.repository.update_to_claimed(listing)

    def delete_listing(self, listing_id: int, user_id: int) -> None:
        listing = self.get_single_listing(listing_id)
        if listing.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bu e'lon sizga tegishli emas",
            )
        self.repository.delete_listing(listing)
