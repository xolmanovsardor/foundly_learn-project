from sqlalchemy.orm import Session
from app.listings.models import ListingModel
from app.listings.schemas import ListingCreateSchema

class ListingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_listings(self, search: str = None, type: str = None, page: int = 1, page_size: int = 20):
        query = self.db.query(ListingModel)
        if search:
            query = query.filter(ListingModel.title.ilike(f"%{search}%"))
        if type:
            query = query.filter(ListingModel.type == type)
        skip = (page - 1) * page_size
        return query.offset(skip).limit(page_size).all()

    # ID bo'yicha topish [oxdFQS]
    def get_listing_by_id(self, listing_id: int) -> ListingModel | None:
        return self.db.query(ListingModel).filter(ListingModel.id == listing_id).first()

    # Statusni CLAIMED qilish [oxdFQS]
    def update_to_claimed(self, listing: ListingModel) -> ListingModel:
        listing.status = "CLAIMED"
        self.db.commit()
        self.db.refresh(listing)
        return listing

    # Yangi e'lon qo'shish (Yangi ustunlar bilan) [oxdFQS]
    def create_new_listing(self, listing_data: ListingCreateSchema, user_id: int) -> ListingModel:
        db_listing = ListingModel(
            title=listing_data.title,
            description=listing_data.description,
            type=listing_data.type,
            location=listing_data.location,      # Qo'shildi
            date_found=listing_data.date_found,  # Qo'shildi
            image_url=listing_data.image_url,
            user_id=user_id
        )
        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return db_listing

class ListingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_listings(self, search: str = None, type: str = None, page: int = 1, page_size: int = 20):
        query = self.db.query(ListingModel)
        if search:
            query = query.filter(ListingModel.title.ilike(f"%{search}%"))
        if type:
            query = query.filter(ListingModel.type == type)
        skip = (page - 1) * page_size
        return query.offset(skip).limit(page_size).all()

    def get_listing_by_id(self, listing_id: int) -> ListingModel | None:
        return self.db.query(ListingModel).filter(ListingModel.id == listing_id).first()

    def update_to_claimed(self, listing: ListingModel) -> ListingModel:
        listing.status = "CLAIMED"
        self.db.commit()
        self.db.refresh(listing)
        return listing

    # Rasmda so'ralgan ma'lumotlarni Publish (Push) qiluvchi asosiy baza funksiyasi [KUCKkU]:
    def create_new_listing(self, listing_data: ListingCreateSchema, user_id: int) -> ListingModel:
        db_listing = ListingModel(
            type=listing_data.type,
            title=listing_data.title,
            description=listing_data.description,
            date_found=listing_data.date_found,
            image_url=listing_data.image_url,
            user_id=user_id
        )
        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return db_listing
