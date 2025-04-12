from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="My Own Personal Claude",
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
    return {"message": "My Own Personal Claude Backend"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Importer et inclure les routers ici une fois qu'ils sont créés
# from app.api.v1 import auth, chat, mcp, monitor
# app.include_router(auth.router)
# app.include_router(chat.router)
# app.include_router(mcp.router)
# app.include_router(monitor.router)
