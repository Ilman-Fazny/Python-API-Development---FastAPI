from pydantic import BaseModel, ConfigDict

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
