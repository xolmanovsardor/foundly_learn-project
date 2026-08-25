from fastapi import FastAPI
from app.core.config import settings
from app.database import engine, Base
from app.users.router import router as users_router
from app.listings.router import router as listings_router  # Импортируем новый роутер

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(users_router)
app.include_router(listings_router)  # Подключаем объявления к FastAPI

@app.get("/")
def root():
    return {"status": "Ishlamoqda", "project": settings.PROJECT_NAME}
