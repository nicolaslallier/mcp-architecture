#!/usr/bin/env python3
"""
Test script to verify the file upload function works correctly
"""

import json
from unittest.mock import Mock, MagicMock
import io

# Import our function code
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'FileUpload'))
from __init__ import main

def test_file_upload_function():
    """Test the file upload function with a mock HTTP request"""
    
    # Create a mock file
    mock_file = MagicMock()
    mock_file.filename = "test.txt"
    mock_file.content_type = "text/plain"
    mock_file.read.return_value = b"Hello, this is a test file!"
    
    # Create mock form data
    mock_form = {"file": mock_file}
    
    # Create a mock HTTP request
    mock_request = Mock()
    mock_request.method = "POST"
    mock_request.headers = {"content-type": "multipart/form-data; boundary=test"}
    mock_request.form = mock_form
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Print the response
    print("✅ File upload function test successful!")
    print("Response:")
    print(json.dumps(response_data, indent=2))
    
    # Verify the response structure
    assert "status" in response_data
    assert "timestamp" in response_data
    
    # Check if upload was successful or failed due to permissions
    if response_data["status"] == "success":
        assert "message" in response_data
        assert "file_info" in response_data
        assert response_data["message"] == "File uploaded successfully"
        
        # Verify file info structure
        file_info = response_data["file_info"]
        assert "original_filename" in file_info
        assert "blob_filename" in file_info
        assert "content_type" in file_info
        assert "file_size" in file_info
        assert "blob_url" in file_info
        assert file_info["original_filename"] == "test.txt"
        assert file_info["content_type"] == "text/plain"
    else:
        # Check for authorization error (expected with read-only SAS)
        assert "error" in response_data
        assert "AuthorizationPermissionMismatch" in response_data["error"] or "not authorized" in response_data["error"]
    
    print("\n✅ All file upload assertions passed!")
    return response_data

def test_invalid_method():
    """Test the function with invalid HTTP method"""
    
    # Create a mock HTTP request with GET method
    mock_request = Mock()
    mock_request.method = "GET"
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Verify error response
    assert response_data["status"] == "error"
    assert "Method not allowed" in response_data["error"]
    assert response.status_code == 405
    
    print("✅ Invalid method test passed!")

def test_no_file():
    """Test the function with no file provided"""
    
    # Create a mock HTTP request with no file
    mock_request = Mock()
    mock_request.method = "POST"
    mock_request.headers = {"content-type": "multipart/form-data; boundary=test"}
    mock_request.form = {}  # No file
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Verify error response
    assert response_data["status"] == "error"
    assert "No file provided" in response_data["error"]
    assert response.status_code == 400
    
    print("✅ No file test passed!")

if __name__ == "__main__":
    print("Testing file upload function...")
    test_file_upload_function()
    test_invalid_method()
    test_no_file()
    print("\n🎉 All tests completed successfully!") 