from pydantic import BaseModel, EmailStr


class GetUser(BaseModel):
    email: EmailStr
