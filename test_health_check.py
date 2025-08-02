#!/usr/bin/env python3
"""
Test script to verify the health check function works correctly
"""

import json
from unittest.mock import Mock

# Import our function code
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'HealthCheck'))
from __init__ import main

def test_health_check_function():
    """Test the health check function with a mock HTTP request"""
    
    # Create a mock HTTP request
    mock_request = Mock()
    mock_request.method = "GET"
    
    # Call our function
    response = main(mock_request)
    
    # Parse the response
    response_data = json.loads(response.get_body().decode('utf-8'))
    
    # Print the response
    print("✅ Health check function test successful!")
    print("Response:")
    print(json.dumps(response_data, indent=2))
    
    # Verify the response structure
    assert "status" in response_data
    assert "timestamp" in response_data
    assert "service" in response_data
    assert "version" in response_data
    assert "system" in response_data
    assert "resources" in response_data
    assert "endpoints" in response_data
    assert response_data["status"] == "healthy"
    assert response_data["service"] == "Azure Function - Hello World API"
    
    print("\n✅ All health check assertions passed!")
    return response_data

if __name__ == "__main__":
    test_health_check_function() 