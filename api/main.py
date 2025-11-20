import sys
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from api.settings import Settings
from api.db.session import async_engine as engine
from api.db import models
from api.routers import agents, auth
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: log starting message
    logger.info("*** Starting %s (env=%s)", settings.app_name, settings.env_name)
    
    # yield control to the application
    yield

    # shutdown: dispose of the async engine
    try:
        await engine.dispose()
    except Exception as e:
        logger.error("Error during engine disposal: %s", e)

    logger.info("*** Shut down %s", settings.app_name)


settings = Settings()

# Initialize the FastAPI app with the application name from settings
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

# Include the auth router with a prefix and tags for better API documentation
app.include_router(auth.router, tags=["auth"])
app.include_router(agents.router, tags=["agents"])

# Root endpoint to verify the application is running.
@app.get("/")
def root():
    return {"message": f"{settings.app_name} is running"}
