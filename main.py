from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.dog_routes import router as dog_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dog_router, prefix="/veterinary")

@app.on_event("startup")
async def startup_db_client():
    print("🚀 FastAPI is running and connected to MongoDB")

@app.get("/")
async def root():
    return {"message": "API is running"}
