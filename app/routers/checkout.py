from fastapi import APIRouter, HTTPException
import httpx

router = APIRouter(prefix="/checkout", tags=["Checkout"])

PESAPAL_BASE = "https://cybqa.pesapal.com/pesapalv3/api"

@router.post("/create-checkout")
async def create_checkout(token: str):
    url = f"{PESAPAL_BASE}/Transactions/SubmitOrderRequest"

    payload = {
        "id": "ORDER-12345",
        "currency": "KES",
        "amount": 100,
        "description": "Test payment",
        "callback_url": "http://localhost:5173/pesapal/callback",
        "notification_id": "YOUR_IPN_ID",
        "billing_address": {
            "email_address": "test@mail.com",
            "phone_number": "0712345678",
            "country_code": "KE"
        }
    }

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.post(
            url,
            json=payload,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )

    if r.status_code != 200:
        raise HTTPException(status_code=502, detail=r.text)

    data = r.json()
    return {
        "order_tracking_id": data.get("order_tracking_id") or data.get("orderTrackingId"),
        "redirect_url": data.get("redirect_url") or data.get("redirectUrl"),
        "raw": data,
    }