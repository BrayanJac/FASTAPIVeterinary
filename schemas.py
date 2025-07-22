def dog_helper(dog) -> dict:
    return {
        "id": str(dog["_id"]),
        "idDog": dog["idDog"],
        "name": dog["name"],
        "breed": dog["breed"],
        "birth_date": str(dog["birth_date"]),
        "human_age": dog["human_age"],
        "dog_age": dog["dog_age"],
        "gender": dog["gender"],
        "owner": dog["owner"],
        "phone": dog["phone"],
    }
