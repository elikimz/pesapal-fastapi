from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.payments import router as payments_router

app = FastAPI(
    title="Pesaflux STK Push API",
    description="FastAPI backend for initiating M-Pesa STK Push payments through Pesaflux.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(payments_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
