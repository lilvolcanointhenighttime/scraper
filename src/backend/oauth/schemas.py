from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    id: int
    login: str
    avatar_url: str