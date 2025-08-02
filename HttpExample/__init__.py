import azure.functions as func
import json
from datetime import datetime


def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that returns a Hello World message via REST API
    """
    try:
        # Get the HTTP method
        method = req.method
        
        # Create response data
        response_data = {
            "message": "Hello, World!",
            "timestamp": datetime.utcnow().isoformat(),
            "method": method,
            "status": "success"
        }
        
        # Return JSON response
        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )
        
    except Exception as e:
        # Return error response if something goes wrong
        error_data = {
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat(),
            "status": "error"
        }
        
        return func.HttpResponse(
            json.dumps(error_data, indent=2),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        ) 