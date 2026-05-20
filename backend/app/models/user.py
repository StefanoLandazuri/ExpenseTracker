from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_password_length

    def validate_password_length(self):
        if len(self.password) < 8:
            raise ValueError("password must be at least 8 characters")


class User(BaseModel):
    id: str
    email: EmailStr
    created_at: str


class UserInDB(User):
    password_hash: str