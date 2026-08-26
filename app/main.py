from fastapi import FastAPI
from app.core.config import settings
from app.database import engine, Base

# --- ДОБАВЬТЕ ЭТИ ДВЕ СТРОКИ ТУТ ---
from app.users.models import UserModel
from app.listings.models import ListingModel
# ----------------------------------

from app.users.router import router as users_router
from app.listings.router import router as listings_router

# Теперь SQLAlchemy увидит все колонки и создаст/обновит таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users_router)
app.include_router(listings_router)

@app.get("/")
def root():
    return {"status": "Ishlamoqda", "project": settings.PROJECT_NAME}
