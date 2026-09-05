import os
import sys

# Self-healing sys.path bootstrap for cloud environments
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import engine, Base
from app.routers import health, auth, prediction, chat, weather, reports, dashboard

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AgriRakshak Backend API — AI-powered agriculture assistant & officer monitoring dashboard"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(prediction.router)
app.include_router(chat.router)
app.include_router(weather.router)
app.include_router(reports.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to AgriRakshak API",
        "docs": "/docs",
        "health": "/health"
    }
