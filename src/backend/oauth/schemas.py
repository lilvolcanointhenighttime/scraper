from pydantic import BaseModel

class UserSchema(BaseModel):
    id: int
    login: str
    avatar_url: str