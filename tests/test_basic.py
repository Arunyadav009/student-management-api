from fastapi.testclient import TestClient
from main import app
import pytest
import uuid

client = TestClient(app)

def test_get_student():
    response = client.get("/students")
    assert response.status_code == 401

def test_register_user(test_email):
    response = client.post(
        "/register",
        json={
            "name": "Test User",
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    print(response.json())

    assert response.status_code == 201
    
    
def test_register_duplicate_user(test_email):
    client.post(
        "/register",
        json={
            "name": "Test User",
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/register",
        json={
            "name": "Another User",
            "email": test_email,
            "password": "AnotherPassword123"
        }
    )

    assert response.status_code == 409
    
    
def test_login_user(test_email):
    client.post(
        "/register",
        json={
            "name": "Login Test User",
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/login",
        json={
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    print(response.json())

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    token = response.json()["access_token"]

    students_response = client.get(
        "/students",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert students_response.status_code == 200
    
    
def test_create_student(authenticated_client, test_department, student_email):

    response = authenticated_client.post(
        "/students",
        json={
            "name": "Test Student",
            "age": 22,
            "course": "Computer Science",
            "email": student_email,
            "department_id": test_department["id"]
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "Test Student"
    assert data["age"] == 22
    assert data["course"] == "Computer Science"
    assert data["email"] == student_email
    assert data["department_id"] == test_department["id"]
    
    
def test_get_students(authenticated_client, test_student):

    response = authenticated_client.get("/students")

    assert response.status_code == 200

    data = response.json()

    assert len(data["students"]) >= 1

    student = next(
        student for student in data["students"]
        if student["id"] == test_student["id"]
    )

    assert student["name"] == "Test Student"
    assert student["age"] == 22
    assert student["course"] == "Computer Science"
    
    
def test_get_student_by_id(authenticated_client, test_student):
    student_id = test_student["id"]

    response = authenticated_client.get(
        f"/students/{student_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["name"] == "Test Student"
    assert data["age"] == 22
    assert data["course"] == "Computer Science"
    
       
def test_get_student_not_found(authenticated_client):

    response = authenticated_client.get("/students/999999")

    assert response.status_code == 404
    
    

def test_update_student(authenticated_client, test_student):

    student_id = test_student["id"]

    response = authenticated_client.put(
        f"/students/{student_id}",
        json={
            "age": 25,
            "course": "Artificial Intelligence"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == student_id
    assert data["age"] == 25
    assert data["course"] == "Artificial Intelligence"

    # Make sure fields we did not update remain unchanged
    assert data["name"] == "Test Student"
    assert data["email"] == test_student["email"]


def test_delete_student(authenticated_client, test_student):

    student_id = test_student["id"]

    response = authenticated_client.delete(
        f"/students/{student_id}"
    )

    assert response.status_code == 204

    # Verify the student was actually deleted
    get_response = authenticated_client.get(
        f"/students/{student_id}"
    )

    assert get_response.status_code == 404


def test_delete_student_not_found(authenticated_client):

    response = authenticated_client.delete(
        "/students/999999"
    )

    assert response.status_code == 404



def test_duplicate_student_email(
    authenticated_client,
    test_department,
    student_email
):

    first_response = authenticated_client.post(
        "/students",
        json={
            "name": "First Student",
            "age": 22,
            "course": "Computer Science",
            "email": student_email,
            "department_id": test_department["id"]
        }
    )

    assert first_response.status_code == 201

    second_response = authenticated_client.post(
        "/students",
        json={
            "name": "Second Student",
            "age": 23,
            "course": "Artificial Intelligence",
            "email": student_email,
            "department_id": test_department["id"]
        }
    )

    assert second_response.status_code == 409

def test_invalid_department(authenticated_client, student_email):

    response = authenticated_client.post(
        "/students",
        json={
            "name": "Test Student",
            "age": 22,
            "course": "Computer Science",
            "email": student_email,
            "department_id": 999999
        }
    )

    assert response.status_code == 400


def test_invalid_student_data(authenticated_client, test_department, student_email):

    response = authenticated_client.post(
        "/students",
        json={
            "name": "Test Student",
            "age": "twenty-two",
            "course": "Computer Science",
            "email": student_email,
            "department_id": test_department["id"]
        }
    )

    assert response.status_code == 422



def test_login_wrong_password(test_email):

    client.post(
        "/register",
        json={
            "name": "Wrong Password User",
            "email": test_email,
            "password": "TestPassword123"
        }
    )

    response = client.post(
        "/login",
        json={
            "email": test_email,
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401


def test_filter_students_by_course(authenticated_client, test_student):

    response = authenticated_client.get(
        "/students",
        params={
            "course": "Computer Science"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["students"]) >= 1

    for student in data["students"]:
        assert student["course"] == "Computer Science"


def test_filter_students_by_min_age(authenticated_client, test_student):

    response = authenticated_client.get(
        "/students",
        params={
            "min_age": 21
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["students"]) >= 1

    for student in data["students"]:
        assert student["age"] >= 21


def test_pagination(authenticated_client, test_student):

    response = authenticated_client.get(
        "/students",
        params={
            "page": 1,
            "limit": 1
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "students" in data
    assert "total" in data
    assert "page" in data
    assert "limit" in data

    assert data["page"] == 1
    assert data["limit"] == 1
    assert len(data["students"]) <= 1


def test_update_student_not_found(authenticated_client):

    response = authenticated_client.put(
        "/students/999999",
        json={
            "age": 25
        }
    )

    assert response.status_code == 404


def test_invalid_update_data(authenticated_client, test_student):
    response = authenticated_client.put(
        f"/students/{test_student['id']}",
        json={
            "age": "twenty-five"
        }
    )

    assert response.status_code == 422
    
    
def test_normal_user_can_read_students(normal_user_client):
    response = normal_user_client.get("/students")

    assert response.status_code == 200



def test_normal_user_cannot_create_student(normal_user_client):
    response = normal_user_client.post(
        "/students",
        json={
            "name": "Unauthorized Student",
            "age": 22,
            "course": "Computer Science",
            "email": f"unauthorized_{uuid.uuid4().hex}@example.com"
        }
    )

    assert response.status_code == 403
    
def test_normal_user_cannot_create_department(normal_user_client):
    response = normal_user_client.post(
        "/departments",
        json={
            "name": f"Unauthorized_{uuid.uuid4().hex[:8]}"
        }
    )

    assert response.status_code == 403