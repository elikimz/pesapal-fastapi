# Pesaflux STK Push FastAPI Backend

This repository contains a clean FastAPI backend for initiating M-Pesa STK Push requests through the Pesaflux API. The backend exposes a single payment endpoint consumed by the frontend UI.

> **Payment flow:** Frontend UI → FastAPI Backend → Pesaflux API → M-Pesa STK Push → User phone.

## Project structure

```text
app/
├── main.py
├── services/
│   └── pesaflux.py
├── routes/
│   └── payments.py
└── core/
    └── config.py
```

## Environment variables

Create a `.env` file from `.env.example` and set the required values. The live credentials should not be hardcoded in source files.

```env
API_KEY=PSFXmLezf0Zf
EMAIL=frankkhayumbi10@gmail.com
PESAFLUX_BASE_URL=https://api.pesaflux.co.ke/v1
REQUEST_TIMEOUT_SECONDS=30
```

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API

### `POST /pay`

Request body:

```json
{
  "amount": "1",
  "phone": "2547XXXXXXXX",
  "reference": "Order 1001"
}
```

The endpoint validates that the phone number is in the `2547XXXXXXXX` format, sends the request to `https://api.pesaflux.co.ke/v1/initiatestk`, and returns the Pesaflux response directly to the frontend.

## Important note

The business name shown in the M-Pesa STK prompt is controlled by Safaricom and Pesaflux. This backend does not attempt to change or hide the **Paying to** name.
