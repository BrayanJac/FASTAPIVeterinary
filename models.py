from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class DogModel(BaseModel):
    idDog: str
    name: str
    breed: str
    birth_date: datetime
    human_age: Optional[int] = None
    dog_age: Optional[int] = None
    gender: str
    owner: str
    phone: str

class UpdateDogModel(BaseModel):
    name: Optional[str]
    breed: Optional[str]
    birth_date: Optional[date]
    gender: Optional[str]
    owner: Optional[str]
    phone: Optional[str]
