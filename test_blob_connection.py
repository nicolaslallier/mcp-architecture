#!/usr/bin/env python3
"""
Test script to verify the blob connection test function works correctly
"""

import json
from unittest.mock import Mock

# Import our function code
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'BlobTest'))
from __init__ import main

def test_blob_connection_function():
    """Test the blob connection test function with a mock HTTP request"""
    
    # Create a mock HTTP request
    mock_request = Mock()
    mock_request.method = "GET"
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Print the response
    print("✅ Blob connection test function successful!")
    print("Response:")
    print(json.dumps(response_data, indent=2))
    
    # Verify the response structure
    assert "status" in response_data
    assert "timestamp" in response_data
    assert "message" in response_data
    assert "container" in response_data
    assert "tests" in response_data
    
    # Verify tests structure
    tests = response_data["tests"]
    assert "connection_test" in tests
    assert "container_access_test" in tests
    assert "read_permission_test" in tests
    assert "write_permission_test" in tests
    assert "delete_permission_test" in tests
    
    print("\n✅ All blob connection test assertions passed!")
    return response_data

if __name__ == "__main__":
    print("Testing blob connection test function...")
    test_blob_connection_function()
    print("\n🎉 All blob connection tests completed successfully!") 