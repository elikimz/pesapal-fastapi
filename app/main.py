"""
Pesaflux Payment API — FastAPI entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import payment

app = FastAPI(
    title="Pesaflux Payment API",
    description="Simple M-Pesa STK Push payment backend powered by Pesaflux.",
    version="2.0.0",
)

# ---------------------------------------------------------------------------
# CORS — allow the React frontend (and any origin during development)
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(payment.router)


@app.get("/")
async def root():
    return {"status": "Pesaflux Payment API running 🚀"}
