# Deploy to Azure App Service

## Option 1: Manual Deployment (Recommended for Testing)

### Prerequisites
- Azure CLI installed: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
- Azure account with active subscription

### Steps

1. **Login to Azure**
```bash
az login
```

2. **Deploy the app**
```bash
az webapp deployment source config-zip \
  --resource-group <your-resource-group> \
  --name pesafluxapi \
  --src pesaflux-api.zip
```

Or use the Azure Portal:
1. Go to your App Service
2. Click "Deployment Center"
3. Select "Local Git" or "GitHub"
4. Follow the prompts

## Option 2: GitHub Integration (Automatic Deployment)

1. **In Azure Portal:**
   - Go to App Service → Deployment Center
   - Select "GitHub" as source
   - Authorize and select your repository
   - Select branch: `main`
   - Click "Save"

2. **Azure will automatically deploy when you push to main**

## Option 3: Using Azure CLI

```bash
# Create resource group
az group create --name pesaflux-rg --location southafricanorth

# Create App Service plan
az appservice plan create \
  --name pesaflux-plan \
  --resource-group pesaflux-rg \
  --sku B1 \
  --is-linux

# Create web app
az webapp create \
  --resource-group pesaflux-rg \
  --plan pesaflux-plan \
  --name pesafluxapi \
  --runtime "PYTHON|3.11"

# Deploy code
az webapp deployment source config-zip \
  --resource-group pesaflux-rg \
  --name pesafluxapi \
  --src <path-to-zip>
```

## Configuration in Azure

Set these environment variables in Azure App Service:

1. Go to **Configuration** → **Application settings**
2. Add the following:

| Name | Value |
|------|-------|
| `DATABASE_URL` | `sqlite:///./pesaflux.db` |
| `PESAFLUX_API_KEY` | `PSFXmLezf0Zf` |
| `PESAFLUX_EMAIL` | `frankkhayumbi10@gmail.com` |
| `DEBUG` | `False` |
| `SECRET_KEY` | `pesaflux-secret-key-2024-production` |

3. Click "Save"

## Verify Deployment

```bash
# Check if app is running
curl https://pesafluxapi-a5dfaaa8h7ebhrfv.southafricanorth-01.azurewebsites.net/health

# Test the payment endpoint
curl -X POST https://pesafluxapi-a5dfaaa8h7ebhrfv.southafricanorth-01.azurewebsites.net/pay \
  -H "Content-Type: application/json" \
  -d '{"amount": "1", "phone": "254712345678", "reference": "Order 1001"}'
```

## Troubleshooting

### Check logs
```bash
az webapp log tail \
  --resource-group pesaflux-rg \
  --name pesafluxapi
```

### Common issues

**500 Error:**
- Check environment variables are set
- Check database file has write permissions
- Check logs for detailed error

**Deployment fails:**
- Ensure `requirements.txt` is in root directory
- Check Python version compatibility (3.9+)
- Verify all dependencies are listed

**Database errors:**
- SQLite database file needs write permissions
- Azure App Service file system is temporary - data may be lost on restart
- For production, use Azure SQL Database instead

## Next Steps

1. ✅ Deploy to Azure
2. ✅ Test the `/pay` endpoint
3. ✅ Configure callback URL in PesaFlux dashboard
4. ✅ Monitor logs for errors
5. ✅ Set up Azure Application Insights for monitoring
