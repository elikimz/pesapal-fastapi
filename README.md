# PesaFlux Payment Integration Backend

A production-ready FastAPI backend for PesaFlux STK Push payments with PostgreSQL database and webhook support.

## Features

- ✅ FastAPI with async support
- ✅ PostgreSQL with SQLAlchemy ORM
- ✅ PesaFlux STK Push integration
- ✅ Webhook callback handling
- ✅ Transaction tracking
- ✅ Error handling and logging
- ✅ Environment-based configuration

## Project Structure

```
app/
├── main.py              # FastAPI app initialization
├── config.py            # Configuration management
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── routers/
│   ├── payments.py      # Payment endpoints
│   └── callbacks.py     # Webhook endpoints
├── services/
│   ├── pesaflux.py      # PesaFlux API client
│   └── transactions.py  # Transaction service
└── database.py          # Database setup
```

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database URL and PesaFlux credentials
```

### 3. Initialize Database

```bash
alembic upgrade head
```

### 4. Run Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /pay
Initiate STK Push payment

**Request:**
```json
{
  "phone": "254712345678",
  "amount": 100
}
```

**Response:**
```json
{
  "status": "success",
  "message": "STK push sent",
  "reference": "TXN123456",
  "data": {...}
}
```

### POST /callback
Receive payment status from PesaFlux

**Request (from PesaFlux):**
```json
{
  "reference": "TXN123456",
  "status": "success",
  "amount": 100,
  "phone": "254712345678"
}
```

### GET /transactions
List all transactions

### GET /transactions/{reference}
Get transaction details

## Database Schema

### transactions table
- id: Primary key
- phone: Customer phone number
- amount: Payment amount
- reference: Unique transaction reference
- status: pending/success/failed
- pesaflux_response: Raw API response
- created_at: Timestamp
- updated_at: Timestamp

## Error Handling

All errors return standardized responses:

```json
{
  "status": "error",
  "message": "Error description",
  "error_code": "ERROR_CODE"
}
```

## Logging

Logs are printed to console. Configure logging in `config.py`.

## Production Deployment

1. Set `DEBUG=False` in `.env`
2. Use a production database (managed PostgreSQL)
3. Set a strong `SECRET_KEY`
4. Configure CORS properly
5. Use HTTPS for callbacks
6. Set up monitoring and alerts
