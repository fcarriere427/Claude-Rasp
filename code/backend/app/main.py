from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import auth
from app.core.config import settings

# Import des routes de test (uniquement en dev/test)
if settings.ENVIRONMENT.lower() != "production":
    from app.api.v1.test import routes as test_routes

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


@app.get(settings.API_V1_STR + "/health")
async def api_health_check():
    return {"status": "ok", "api_version": "v1"}


# Include routers
app.include_router(auth.router, prefix=settings.API_V1_STR)

# Routes de test (uniquement en dev/test)
if settings.ENVIRONMENT.lower() != "production":
    app.include_router(test_routes.router)

# TODO: Uncomment when implemented
# app.include_router(chat.router, prefix=settings.API_V1_STR)
# app.include_router(mcp.router, prefix=settings.API_V1_STR)
# app.include_router(monitor.router, prefix=settings.API_V1_STR)
