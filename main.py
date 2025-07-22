from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.dog_routes import router as dog_router
import os
import uvicorn

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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
