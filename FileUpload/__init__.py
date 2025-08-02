import azure.functions as func
import json
import logging
import uuid
from datetime import datetime
import os
from azure.storage.blob import BlobServiceClient, ContentSettings
import tempfile
import mimetypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure Blob Storage configuration
BLOB_SAS_URL = "https://stdofsprdcae.blob.core.windows.net/mcpai?sp=racwdl&st=2025-08-02T14:10:50Z&se=2026-08-02T22:25:50Z&spr=https&sv=2024-11-04&sr=c&sig=zEd8CjW0q34r%2Bcigml1L5eLy6kcLBN1xescpUdEyk7w%3D"
CONTAINER_NAME = "mcpai"

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that handles file upload to Azure Blob Storage
    """
    try:
        # Check if the request is a POST
        if req.method != "POST":
            return func.HttpResponse(
                json.dumps({
                    "error": "Method not allowed. Only POST is supported.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error"
                }, indent=2),
                status_code=405,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            )

        # Get the content type
        content_type = req.headers.get('content-type', '')
        
        # Handle multipart form data
        if 'multipart/form-data' in content_type:
            return handle_multipart_upload(req)
        else:
            return func.HttpResponse(
                json.dumps({
                    "error": "Content-Type must be multipart/form-data",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error"
                }, indent=2),
                status_code=400,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            )

    except Exception as e:
        logger.error(f"Error in file upload: {str(e)}")
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

def handle_multipart_upload(req: func.HttpRequest) -> func.HttpResponse:
    """
    Handle multipart form data upload
    """
    try:
        # Get the form data
        form_data = req.form
        
        # Check if file is present
        if 'file' not in form_data:
            return func.HttpResponse(
                json.dumps({
                    "error": "No file provided. Please include a file in the 'file' field.",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error"
                }, indent=2),
                status_code=400,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            )

        file_data = form_data['file']
        
        # Validate file data
        if not hasattr(file_data, 'filename') or not file_data.filename:
            return func.HttpResponse(
                json.dumps({
                    "error": "Invalid file data",
                    "timestamp": datetime.utcnow().isoformat(),
                    "status": "error"
                }, indent=2),
                status_code=400,
                headers={
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            )

        # Generate unique filename
        original_filename = file_data.filename
        file_extension = os.path.splitext(original_filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        
        # Get file content
        file_content = file_data.read()
        
        # Upload to Azure Blob Storage
        blob_url = upload_to_blob_storage(unique_filename, file_content, file_data.content_type)
        
        # Return success response
        response_data = {
            "status": "success",
            "timestamp": datetime.utcnow().isoformat(),
            "message": "File uploaded successfully",
            "file_info": {
                "original_filename": original_filename,
                "blob_filename": unique_filename,
                "content_type": file_data.content_type,
                "file_size": len(file_content),
                "blob_url": blob_url
            }
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
        logger.error(f"Error handling multipart upload: {str(e)}")
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

def upload_to_blob_storage(filename: str, file_content: bytes, content_type: str) -> str:
    """
    Upload file to Azure Blob Storage
    """
    try:
        # Create blob service client using the SAS URL
        blob_service_client = BlobServiceClient(account_url=BLOB_SAS_URL)
        container_client = blob_service_client.get_container_client(CONTAINER_NAME)
        
        # Get blob client
        blob_client = container_client.get_blob_client(filename)
        
        # Upload the file
        blob_client.upload_blob(
            file_content,
            overwrite=True,
            content_settings=ContentSettings(content_type=content_type)
        )
        
        # Return the blob URL
        return blob_client.url
        
    except Exception as e:
        logger.error(f"Error uploading to blob storage: {str(e)}")
        raise Exception(f"Failed to upload file to blob storage: {str(e)}") 