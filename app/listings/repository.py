from sqlalchemy.orm import Session
from app.listings.models import ListingModel
from app.listings.schemas import ListingCreateSchema
from app.users.models import UserModel

class ListingRepository:
    def __init__(self, db: Session):
        self.db = db

    # 1. Filtrlash va qidiruv bilan barcha e'lonlarni olish
    def get_all_listings(self, search: str = None, type: str = None, page: int = 1, page_size: int = 20):
        query = self._filtered_query(search=search, type=type)
        skip = (page - 1) * page_size
        return query.order_by(ListingModel.id.desc()).offset(skip).limit(page_size).all()

    def get_user_listings(self, user_email: str, search: str = None, type: str = None, page: int = 1, page_size: int = 20):
        query = self._filtered_query(search=search, type=type).join(
            UserModel, ListingModel.user_id == UserModel.id
        ).filter(UserModel.email == user_email)
        skip = (page - 1) * page_size
        return query.order_by(ListingModel.id.desc()).offset(skip).limit(page_size).all()

    def _filtered_query(self, search: str = None, type: str = None):
        query = self.db.query(ListingModel)
        if search:
            query = query.filter(
                (ListingModel.title.ilike(f"%{search}%")) |
                (ListingModel.description.ilike(f"%{search}%"))
            )
        if type:
            query = query.filter(ListingModel.type == type)
        return query

    # 2. ID bo'yicha topish
    def get_listing_by_id(self, listing_id: int) -> ListingModel | None:
        return self.db.query(ListingModel).filter(ListingModel.id == listing_id).first()

    # 3. Statusni CLAIMED qilish
    def update_to_claimed(self, listing: ListingModel) -> ListingModel:
        listing.status = "CLAIMED"
        self.db.commit()
        self.db.refresh(listing)
        return listing

    def delete_listing(self, listing: ListingModel) -> None:
        self.db.delete(listing)
        self.db.commit()

    # 4. Yangi e'lon qo'shish
    def create_new_listing(self, listing_data: ListingCreateSchema, user_id: int) -> ListingModel:
        # Har ikkala variantdagi maydonlarni xavfsiz birlashtiramiz
        db_listing = ListingModel(
            title=listing_data.title,
            description=listing_data.description,
            type=listing_data.type,
            date_found=listing_data.date_found,
            image_url=listing_data.image_url,
            user_id=user_id
        )
        # Agar modelingizda location ustuni bo'lsa, pastdagi qatorni ochib qo'ying:
        # if hasattr(listing_data, 'location'): db_listing.location = listing_data.location

        self.db.add(db_listing)
        self.db.commit()
        self.db.refresh(db_listing)
        return db_listing
