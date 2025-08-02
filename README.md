# Azure Function - Hello World API

This project contains an Azure Function that provides a REST API endpoint returning a "Hello, World!" message.

## Project Structure

```
mcp-architecture/
├── HttpExample/
│   ├── __init__.py          # Main function code
│   └── function.json        # Function configuration
├── host.json                # Azure Functions host configuration
├── local.settings.json      # Local development settings
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

- **REST API Endpoint**: `/api/hello`
- **HTTP Methods**: GET and POST
- **Response Format**: JSON with message, timestamp, and method information
- **CORS Support**: Configured for cross-origin requests
- **Error Handling**: Proper error responses with status codes

## Local Development

### Prerequisites

1. **Python 3.8+** installed
2. **Azure Functions Core Tools** installed
3. **Azure Storage Emulator** (optional, for local development)

### Installation

1. Install Azure Functions Core Tools:
   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

1. Start the function app:
   ```bash
   func start
   ```

2. The function will be available at:
   ```
   http://localhost:7071/api/hello
   ```

### Testing the API

#### Using curl:
```bash
# GET request
curl http://localhost:7071/api/hello

# POST request
curl -X POST http://localhost:7071/api/hello
```

#### Using PowerShell:
```powershell
# GET request
Invoke-RestMethod -Uri "http://localhost:7071/api/hello" -Method Get

# POST request
Invoke-RestMethod -Uri "http://localhost:7071/api/hello" -Method Post
```

#### Expected Response:
```json
{
  "message": "Hello, World!",
  "timestamp": "2024-01-15T10:30:45.123456",
  "method": "GET",
  "status": "success"
}
```

## Deployment to Azure

### Prerequisites

1. **Azure CLI** installed and authenticated
2. **Azure Functions App** created in Azure

### Deployment Steps

1. Create a Function App in Azure (if not exists):
   ```bash
   az functionapp create --resource-group <resource-group-name> --consumption-plan-location <location> --runtime python --runtime-version 3.9 --functions-version 4 --name <function-app-name> --storage-account <storage-account-name>
   ```

2. Deploy the function:
   ```bash
   func azure functionapp publish <function-app-name>
   ```

3. The function will be available at:
   ```
   https://<function-app-name>.azurewebsites.net/api/hello
   ```

## API Documentation

### Endpoint: `/api/hello`

**URL**: `https://<your-function-app>.azurewebsites.net/api/hello`

**Methods**: GET, POST

**Authentication**: Anonymous

**Response Format**: JSON

**Success Response (200)**:
```json
{
  "message": "Hello, World!",
  "timestamp": "2024-01-15T10:30:45.123456",
  "method": "GET",
  "status": "success"
}
```

**Error Response (500)**:
```json
{
  "error": "Error message",
  "timestamp": "2024-01-15T10:30:45.123456",
  "status": "error"
}
```

## Development Notes

- The function supports both GET and POST methods
- CORS is enabled for cross-origin requests
- All responses include a timestamp in ISO format
- Error handling is implemented with proper HTTP status codes
- The function is configured for Python 3.9+ runtime

## Next Steps

To extend this function, you can:
1. Add query parameters support
2. Implement request body parsing for POST requests
3. Add authentication and authorization
4. Integrate with Azure services (Storage, Database, etc.)
5. Add logging and monitoring