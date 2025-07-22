from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = os.getenv("MONGO_DETAILS")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client["veterinaria"]
dog_collection = database["dogs"]
