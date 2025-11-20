from fastapi import FastAPI
import models
from db_postgres import engine
from routers import agents, topics, topic_instructions, users
from fastapi.middleware.cors import CORSMiddleware

# Ensure all tables are created in the database
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the users router with a prefix and tags for better API documentation
app.include_router(users.router, prefix="/api", tags=["users"])

# Include the agents router with a prefix and tags for better API documentation
app.include_router(agents.router, prefix="/api", tags=["agents"])

# Include the topics router with a prefix and tags for better API documentation
app.include_router(topics.router, prefix="/api", tags=["topics"])

# Include the topic instructions router with a prefix and tags for better API documentation
app.include_router(topic_instructions.router, prefix="/api", tags=["topic_instructions"])

# Root endpoint to verify the application is running
@app.get("/")
def root():
    return {"message": "Agent Builder API is running"}
