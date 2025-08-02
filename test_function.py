#!/usr/bin/env python3
"""
Test script to verify the Azure Function code works correctly
"""

import json
from datetime import datetime
from unittest.mock import Mock

# Import our function code
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'HttpExample'))
from __init__ import main

def test_hello_function():
    """Test the hello function with a mock HTTP request"""
    
    # Create a mock HTTP request
    mock_request = Mock()
    mock_request.method = "GET"
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Print the response
    print("✅ Function test successful!")
    print("Response:")
    print(json.dumps(response_data, indent=2))
    
    # Verify the response structure
    assert "message" in response_data
    assert "timestamp" in response_data
    assert "method" in response_data
    assert "status" in response_data
    assert response_data["message"] == "Hello, World!"
    assert response_data["method"] == "GET"
    assert response_data["status"] == "success"
    
    print("\n✅ All assertions passed!")
    return response_data

if __name__ == "__main__":
    test_hello_function() 