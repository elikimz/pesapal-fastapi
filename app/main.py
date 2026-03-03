from fastapi import FastAPI

app = FastAPI(title="Pesapal API")



from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import payments, pesapal,checkout

app = FastAPI()

# ----------------------------
# CORS Middleware (updated)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ only for testing!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Include Routers
# ----------------------------
app.include_router(payments.router)
app.include_router(pesapal.router)
app.include_router(checkout.router)





@app.get("/")
async def root():
    return {"status": "API running 🚀"}