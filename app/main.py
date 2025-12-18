from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, searches, payment

app = FastAPI(
    title="E-commerce API",
    description="Backend API para loja virtual com integração M-Pesa",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(searches.router)
app.include_router(payment.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Technical Documentation Analyzer API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


