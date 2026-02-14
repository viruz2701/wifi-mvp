from pydantic import BaseModel

class LocalLogin(BaseModel):
    username: str
    password: str
    mac: str
    venue_id: int