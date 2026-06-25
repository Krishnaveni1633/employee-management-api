import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Test 1 - Root endpoint
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Employee Management API is running!"}
    print("✅ Test 1 Passed: Root endpoint works")

# Test 2 - Register user
def test_register():
    response = client.post("/register", json={
        "name": "Test User",
        "email": "testuser@test.com",
        "password": "testpassword123",
        "role": "admin"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@test.com"
    assert response.json()["role"] == "admin"
    print("✅ Test 2 Passed: User registration works")

# Test 3 - Login
def test_login():
    # First register
    client.post("/register", json={
        "name": "Login Test",
        "email": "logintest@test.com",
        "password": "testpassword123",
        "role": "admin"
    })
    # Then login
    response = client.post("/login", data={
        "username": "logintest@test.com",
        "password": "testpassword123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    print("✅ Test 3 Passed: Login works")

# Test 4 - Login with wrong password
def test_login_wrong_password():
    response = client.post("/login", data={
        "username": "logintest@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    print("✅ Test 4 Passed: Wrong password rejected")

# Test 5 - Access protected route without token
def test_protected_route_without_token():
    response = client.get("/employees")
    assert response.status_code == 401
    print("✅ Test 5 Passed: Protected route blocks unauthorized access")

# Test 6 - Add employee as admin
def test_add_employee():
    # Register admin
    client.post("/register", json={
        "name": "Admin Test",
        "email": "admintest@test.com",
        "password": "testpassword123",
        "role": "admin"
    })
    # Login
    login = client.post("/login", data={
        "username": "admintest@test.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]

    # Add employee
    response = client.post("/employees",
        json={
            "name": "Test Employee",
            "email": "testemployee@test.com",
            "department": "Technology",
            "position": "Developer",
            "salary": 75000
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Employee"
    print("✅ Test 6 Passed: Admin can add employee")

# Test 7 - Employee role cannot add employee
def test_employee_cannot_add():
    # Register employee role user
    client.post("/register", json={
        "name": "Normal User",
        "email": "normaluser@test.com",
        "password": "testpassword123",
        "role": "employee"
    })
    # Login
    login = client.post("/login", data={
        "username": "normaluser@test.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]

    # Try to add employee
    response = client.post("/employees",
        json={
            "name": "Should Fail",
            "email": "shouldfail@test.com",
            "department": "HR",
            "position": "Manager",
            "salary": 50000
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403
    print("✅ Test 7 Passed: Employee role blocked from adding")

# Test 8 - Get employees
def test_get_employees():
    # Register manager
    client.post("/register", json={
        "name": "Manager Test",
        "email": "managertest@test.com",
        "password": "testpassword123",
        "role": "manager"
    })
    # Login
    login = client.post("/login", data={
        "username": "managertest@test.com",
        "password": "testpassword123"
    })
    token = login.json()["access_token"]

    # Get employees
    response = client.get("/employees",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert "employees" in response.json()
    assert "total" in response.json()
    print("✅ Test 8 Passed: Manager can view employees")