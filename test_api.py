import httpx
import time

BASE_URL = "http://127.0.0.1:8000/api/classify"

def test_valid_name():
    print("Testing valid name (john)...")
    response = httpx.get(f"{BASE_URL}?name=john")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "data" in data
    assert data["data"]["name"] == "john"
    assert "is_confident" in data["data"]
    assert "processed_at" in data["data"]

def test_missing_name():
    print("\nTesting missing name parameter...")
    response = httpx.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert "Missing or empty" in data["message"]

def test_empty_name():
    print("\nTesting empty name parameter...")
    response = httpx.get(f"{BASE_URL}?name=")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert "Missing or empty" in data["message"]

def test_not_a_string():
    print("\nTesting name is not a string (passing list)...")
    # Passing multiple names should trigger 422 in many frameworks
    response = httpx.get(f"{BASE_URL}?name=a&name=b")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert "name is not a string" in data["message"]

def test_not_a_string_bracket():
    print("\nTesting name is not a string (passing bracket list)...")
    response = httpx.get(f"{BASE_URL}?name[]=a")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"

def test_no_prediction():
    print("\nTesting no prediction available (xyzabc123)...")
    response = httpx.get(f"{BASE_URL}?name=xyzabc123")
    print(f"Status: {response.status_code}")
    print(f"Body: {response.text}")
    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "error"
    assert "No prediction available" in data["message"]

if __name__ == "__main__":
    try:
        test_valid_name()
        test_missing_name()
        test_empty_name()
        test_not_a_string()
        test_no_prediction()
        print("\nAll tests passed!")
    except Exception as e:
        print(f"\nTest failed: {e}")
