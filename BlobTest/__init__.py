import azure.functions as func
import json
import logging
from datetime import datetime
from azure.storage.blob import BlobServiceClient
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure Blob Storage configuration
BLOB_SAS_URL = "https://stdofsprdcae.blob.core.windows.net/mcpai?sp=racwdl&st=2025-08-02T14:10:50Z&se=2026-08-02T22:25:50Z&spr=https&sv=2024-11-04&sr=c&sig=zEd8CjW0q34r%2Bcigml1L5eLy6kcLBN1xescpUdEyk7w%3D"
CONTAINER_NAME = "mcpai"

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that tests the connection to Azure Blob Storage
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

        # Test blob storage connection
        test_results = test_blob_storage_connection()
        
        # Return success response
        response_data = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "Blob storage connection test completed",
            "container": CONTAINER_NAME,
            "tests": test_results
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
        logger.error(f"Error testing blob storage connection: {str(e)}")
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

def test_blob_storage_connection() -> dict:
    """
    Test various aspects of blob storage connection
    """
    test_results = {
        "connection_test": {"status": "failed", "message": "", "duration_ms": 0},
        "container_access_test": {"status": "failed", "message": "", "duration_ms": 0},
        "read_permission_test": {"status": "failed", "message": "", "duration_ms": 0},
        "write_permission_test": {"status": "failed", "message": "", "duration_ms": 0},
        "delete_permission_test": {"status": "failed", "message": "", "duration_ms": 0}
    }
    
    try:
        # Test 1: Basic connection
        start_time = time.time()
        blob_service_client = BlobServiceClient(account_url=BLOB_SAS_URL)
        test_results["connection_test"]["status"] = "passed"
        test_results["connection_test"]["message"] = "Successfully connected to blob service"
        test_results["connection_test"]["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        
        # Test 2: Container access
        start_time = time.time()
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        container_properties = container_client.get_container_properties()
        test_results["container_access_test"]["status"] = "passed"
        test_results["container_access_test"]["message"] = f"Container '{CONTAINER_NAME}' accessible"
        test_results["container_access_test"]["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        
        # Test 3: Read permission (list blobs)
        start_time = time.time()
        blob_list = list(container_client.list_blobs(max_results=1))
        test_results["read_permission_test"]["status"] = "passed"
        test_results["read_permission_test"]["message"] = f"Read permission confirmed, found {len(blob_list)} blobs"
        test_results["read_permission_test"]["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        
        # Test 4: Write permission (upload test file)
        start_time = time.time()
        test_blob_name = f"connection-test-{int(time.time())}.txt"
        test_content = f"Connection test file created at {datetime.utcnow().isoformat()}"
        
        blob_client = container_client.get_blob_client(test_blob_name)
        blob_client.upload_blob(test_content, overwrite=True)
        test_results["write_permission_test"]["status"] = "passed"
        test_results["write_permission_test"]["message"] = f"Write permission confirmed, uploaded test file: {test_blob_name}"
        test_results["write_permission_test"]["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        
        # Test 5: Delete permission (clean up test file)
        start_time = time.time()
        blob_client.delete_blob()
        test_results["delete_permission_test"]["status"] = "passed"
        test_results["delete_permission_test"]["message"] = f"Delete permission confirmed, deleted test file: {test_blob_name}"
        test_results["delete_permission_test"]["duration_ms"] = round((time.time() - start_time) * 1000, 2)
        
    except Exception as e:
        # Update the failed test with error details
        for test_name, test_result in test_results.items():
            if test_result["status"] == "failed":
                test_result["message"] = f"Test failed: {str(e)}"
                break
    
    return test_results 