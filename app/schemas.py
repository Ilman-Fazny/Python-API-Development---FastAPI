from pydantic import BaseModel, ConfigDict, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)