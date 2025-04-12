from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth
from app.core.config import settings

app = FastAPI(
    title="Claude API Application",
    description="Application web pour interagir avec l'API Claude sur Raspberry Pi",
    version="0.1.0",
)

# Configuration CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "https://claude.letsq.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Claude API Application Backend"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
# TODO: Uncomment when implemented
# app.include_router(chat.router, prefix=settings.API_V1_STR)
# app.include_router(mcp.router, prefix=settings.API_V1_STR)
# app.include_router(monitor.router, prefix=settings.API_V1_STR)
