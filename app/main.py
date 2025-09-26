from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers.feed import router as feed_router
from .routers.data_collection import router as data_collection_router
from .database import engine
from .models import Base
from .services.data_collection import collect_all_data
import logging

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Video Recommendation Engine", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(feed_router)
app.include_router(data_collection_router)

@app.on_event("startup")
async def startup_event():
    try:
        logging.info("Starting data collection...")
        await collect_all_data()
        logging.info("Data collection completed.")
    except Exception as e:
        logging.warning(f"Data collection failed: {e}. Using sample data instead.")

@app.get("/")
def read_root():
    return {"message": "Video Recommendation Engine API"}
