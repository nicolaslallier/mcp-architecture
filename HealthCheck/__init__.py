import azure.functions as func
import json
import platform
import psutil
from datetime import datetime
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that provides health check information
    """
    try:
        # Get system information
        system_info = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Azure Function - Hello World API",
            "version": "1.0.0",
            "environment": os.getenv("FUNCTIONS_WORKER_RUNTIME", "python"),
            "system": {
                "platform": platform.system(),
                "platform_version": platform.version(),
                "python_version": platform.python_version(),
                "architecture": platform.architecture()[0]
            },
            "resources": {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "memory_available": psutil.virtual_memory().available,
                "memory_total": psutil.virtual_memory().total
            },
            "endpoints": {
                "hello": "/api/hello",
                "health": "/api/health"
            }
        }
        
        # Return JSON response
        return func.HttpResponse(
            json.dumps(system_info, indent=2),
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except Exception as e:
        # Return error response if something goes wrong
        error_data = {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
            "service": "Azure Function - Hello World API"
        }
        
        return func.HttpResponse(
            json.dumps(error_data, indent=2),
            status_code=503,  # Service Unavailable
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        ) 