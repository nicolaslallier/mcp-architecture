#!/usr/bin/env python3
"""
Test script to verify the blob list function works correctly
"""

import json
from unittest.mock import Mock

# Import our function code
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'BlobList'))
from __init__ import main

def test_blob_list_function():
    """Test the blob list function with a mock HTTP request"""
    
    # Create a mock HTTP request
    mock_request = Mock()
    mock_request.method = "GET"
    mock_request.params = {}
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Print the response
    print("✅ Blob list function test successful!")
    print("Response:")
    print(json.dumps(response_data, indent=2))
    
    # Verify the response structure
    assert "status" in response_data
    assert "timestamp" in response_data
    assert "message" in response_data
    assert "container" in response_data
    assert "blobs" in response_data
    assert "total_count" in response_data
    
    print("\n✅ All blob list assertions passed!")
    return response_data

def test_blob_list_with_prefix():
    """Test the blob list function with a prefix parameter"""
    
    # Create a mock HTTP request with prefix
    mock_request = Mock()
    mock_request.method = "GET"
    mock_request.params = {"prefix": "test", "max_results": "10"}
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Verify the response structure
    assert response_data["prefix"] == "test"
    assert response_data["max_results"] == 10
    
    print("✅ Blob list with prefix test passed!")

if __name__ == "__main__":
    print("Testing blob list function...")
    test_blob_list_function()
    test_blob_list_with_prefix()
    print("\n🎉 All blob list tests completed successfully!") 