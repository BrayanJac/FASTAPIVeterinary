from fastapi import APIRouter, HTTPException
from models import DogModel, UpdateDogModel
from database import dog_collection
from schemas import dog_helper
from bson import ObjectId
from datetime import datetime, date


router = APIRouter()

def calculate_human_age(birth_date: datetime) -> int:
    today = datetime.now()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def calculate_dog_age(human_age: int) -> int:
    if human_age == 1:
        return 15
    elif human_age == 2:
        return 24
    elif human_age >= 3:
        return 24 + (human_age - 2) * 4
    return 0

@router.post("/dog", response_model=dict)
async def create_dog(dog: DogModel):
    birth_date_obj = dog.birth_date
    human_age = calculate_human_age(birth_date_obj)
    dog_age = calculate_dog_age(human_age)

    dog_dict = dog.dict()
    if isinstance(dog_dict["birth_date"], date) and not isinstance(dog_dict["birth_date"], datetime):
        dog_dict["birth_date"] = datetime.combine(dog_dict["birth_date"], datetime.min.time())
    dog_dict["human_age"] = human_age
    dog_dict["dog_age"] = dog_age

    new_dog = await dog_collection.insert_one(dog_dict)
    created_dog = await dog_collection.find_one({"_id": new_dog.inserted_id})
    return dog_helper(created_dog)

@router.get("/dogs", response_model=list)
async def get_dogs():
    dogs = []
    async for dog in dog_collection.find():
        dogs.append(dog_helper(dog))
    return dogs

@router.get("/dog/{id}", response_model=dict)
async def get_dog(id: str):
    dog = await dog_collection.find_one({"_id": ObjectId(id)})
    if dog:
        return dog_helper(dog)
    raise HTTPException(status_code=404, detail="Dog not found")

@router.put("/dog/{id}", response_model=dict)
async def update_dog(id: str, dog_data: UpdateDogModel):
    update_data = {k: v for k, v in dog_data.dict().items() if v is not None}
    
    if "birth_date" in update_data:
        human_age = calculate_human_age(update_data["birth_date"])
        dog_age = calculate_dog_age(human_age)
        update_data["human_age"] = human_age
        update_data["dog_age"] = dog_age

    result = await dog_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 1:
        updated_dog = await dog_collection.find_one({"_id": ObjectId(id)})
        return dog_helper(updated_dog)
    raise HTTPException(status_code=404, detail="Dog not found")

@router.delete("/dog/{id}")
async def delete_dog(id: str):
    result = await dog_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return {"message": "Dog deleted"}
    raise HTTPException(status_code=404, detail="Dog not found")
