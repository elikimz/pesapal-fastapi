# Pesaflux Payment API

A minimal FastAPI backend that initiates M-Pesa STK Push payments via [Pesaflux](https://api.pesaflux.co.ke).

## Setup

```bash
cp .env.example .env
# Edit .env and fill in your Pesaflux credentials
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables

| Variable | Description |
|---|---|
| `PESAFLUX_API_KEY` | API key from your Pesaflux Linked Accounts page |
| `PESAFLUX_EMAIL` | Email used to log in to Pesaflux |
| `PESAFLUX_BASE_URL` | Defaults to `https://api.pesaflux.co.ke` |
| `DATABASE_URL` | PostgreSQL async URL (e.g. `postgresql+asyncpg://...`) |

## API Endpoints

### `POST /payment/initiate`

Initiate an STK Push to the customer's phone.

**Request body:**
```json
{
  "phone": "0712345678",
  "amount": 100
}
```

**Response:**
```json
{
  "success": true,
  "message": "Request sent successfully.",
  "transaction_request_id": "SOFTPID...",
  "raw": { ... }
}
```

### `POST /payment/status`

Check the status of a previously initiated transaction.

**Request body:**
```json
{
  "transaction_request_id": "SOFTPID..."
}
```

### `GET /`

Health check — returns `{"status": "Pesaflux Payment API running 🚀"}`.

## Docs

Interactive API docs available at `http://localhost:8000/docs` when running locally.
