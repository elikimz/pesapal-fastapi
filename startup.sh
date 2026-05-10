#!/bin/bash

# PesaFlux API Startup Script for Azure App Service

echo "Starting PesaFlux API..."

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run the application
gunicorn -w 4 -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker app.main:app
