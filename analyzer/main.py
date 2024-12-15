import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import data

app = FastAPI(
    title="ML Uvelka Analyzer API",
    version="0.0.1",
    root_path="/analyzer",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(data.router)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8001
    uvicorn.run(app, host=host, port=port)
