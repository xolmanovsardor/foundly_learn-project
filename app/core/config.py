from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str
    ENVIRONMENT: str
    API_V1_PREFIX: str
    
    # Server sozlamalari
    HOST: str
    PORT: int
    
    # Ma'lumotlar bazasi sozlamalari (PostgreSQL uchun)
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Dinamik ravishda PostgreSQL DATABASE_URL yaratish
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # .env faylini o'qish va ortiqcha maydonlarga ruxsat berish
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="allow"  # Ortiqcha kalitlar kelsa xato bermasligi uchun
    )

settings = Settings()
