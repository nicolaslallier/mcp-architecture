import azure.functions as func
import json
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure Blob Storage configuration
BLOB_SAS_URL = "https://stdofsprdcae.blob.core.windows.net/mcpai?sp=racwdl&st=2025-08-02T14:10:50Z&se=2026-08-02T22:25:50Z&spr=https&sv=2024-11-04&sr=c&sig=zEd8CjW0q34r%2Bcigml1L5eLy6kcLBN1xescpUdEyk7w%3D"
CONTAINER_NAME = "mcpai"

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that lists all blobs in the Azure Blob Storage container
    """
    try:
        # Check if the request is a GET
        if req.method != "GET":
            return func.HttpResponse(
                json.dumps({
                    "error": "Method not allowed. Only GET is supported.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error"
                }, indent=2),
                status_code=405,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            )

        # Get query parameters
        prefix = req.params.get('prefix', '')
        max_results = int(req.params.get('max_results', 50))
        
        # List blobs in the container
        blobs = list_blobs_in_container(prefix, max_results)
        
        # Return success response
        response_data = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Blob list retrieved successfully",
            "container": CONTAINER_NAME,
            "prefix": prefix,
            "max_results": max_results,
            "total_count": len(blobs),
            "blobs": blobs
        }
        
        return func.HttpResponse(
            json.dumps(response_data, indent=2),
            status_code=200,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )

    except Exception as e:
        logger.error(f"Error listing blobs: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error"
            }, indent=2),
            status_code=500,
            headers={
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        )

def list_blobs_in_container(prefix: str = '', max_results: int = 50) -> list:
    """
    List all blobs in the container
    """
    try:
        # Create blob service client using the SAS URL
        blob_service_client = BlobServiceClient(account_url=BLOB_SAS_URL)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # List blobs
        blobs = []
        blob_list = container_client.list_blobs(name_starts_with=prefix, max_results=max_results)
        
        for blob in blob_list:
            blob_info = {
                "name": blob.name,
                "size": blob.size,
                "content_type": blob.content_settings.content_type if blob.content_settings else None,
                "last_modified": blob.last_modified.isoformat() if blob.last_modified else None,
                "etag": blob.etag,
                "url": f"https://stdofsprdcae.blob.core.windows.net/mcpai/{blob.name}"
            }
            blobs.append(blob_info)
        
        return blobs
        
    except Exception as e:
        logger.error(f"Error listing blobs in container: {str(e)}")
        raise Exception(f"Failed to list blobs in container: {str(e)}") 