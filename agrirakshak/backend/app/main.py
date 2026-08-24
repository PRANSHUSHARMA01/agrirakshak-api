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
    allow_origins=settings.cors_origins_list,
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
