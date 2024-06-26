import requests
import json
import pytest

BASE_URL = "http://127.0.0.1:54321/functions/v1/hello-world"
HEADERS = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0",  # Replace with actual token
    "Content-Type": "application/json"
}

def test_edge_function_valid_request():
    data = {"name": "Functions"}
    response = requests.post(BASE_URL, headers=HEADERS, data=json.dumps(data))
    
    assert response.status_code == 200
    assert response.json() == {"message": "Hello Functions!"}

def test_edge_function_missing_param():
    response = requests.post(BASE_URL, headers=HEADERS, data=json.dumps({}))
    
    # Adjust this based on actual function behavior for missing parameter
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World!"}

def test_edge_function_invalid_jwt():
    invalid_headers = HEADERS.copy()
    invalid_headers["Authorization"] = "Bearer invalid_token"
    
    data = {"name": "Functions"}
    response = requests.post(BASE_URL, headers=invalid_headers, data=json.dumps(data))
    
    assert response.status_code == 401

def test_edge_function_no_auth():
    headers_no_auth = HEADERS.copy()
    del headers_no_auth["Authorization"]
    
    data = {"name": "Functions"}
    response = requests.post(BASE_URL, headers=headers_no_auth, data=json.dumps(data))
    
    assert response.status_code == 401
