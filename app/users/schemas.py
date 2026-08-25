from pydantic import BaseModel, EmailStr, model_validator

# 1. Ro'yxatdan o'tish uchun sxema (oldindan bor edi)
class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    password_repeat: str

    @model_validator(mode="after")
    def verify_password_match(self):
        if self.password != self.password_repeat:
            raise ValueError("Parollar bir-biriga mos kelmadi!")
        return self

# 2. Ro'yxatdan o'tgandan keyin foydalanuvchiga qaytadigan javob
class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

# 3. TIZIMGA KIRISH (LOGIN) UCHUN SXEMA (Hozirgi xatoni tuzatadigan qism)
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str

# 4. JWT TOKEN QAYTADIGAN SXEMA
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"

from pydantic import BaseModel, EmailStr

# Oldingi sxemalar tagidan shuni qo'shing:
class ProfileResponseSchema(BaseModel):
    id: int
    first_name: str
    email: EmailStr
    total_listings: int     # Jami e'lonlar soni [_tY6yy]
    active_listings: int    # Faol e'lonlar soni [_tY6yy]
    received_listings: int  # Claim qilingan e'lonlar soni [_tY6yy]

    class Config:
        from_attributes = True
