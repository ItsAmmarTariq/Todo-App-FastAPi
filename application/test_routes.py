from fastapi.testclient import TestClient
from datetime import datetime
from .routes import router

client = TestClient(router)

acces_token_global = []
get_date=datetime.now()



def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_register_user():
    response=client.post("/register/",json={
        "name":"Ali Haider",
        "email":"alihaider12@gmail.com",
        "username":"alihaider1",
        "password":"alihaider123"
    },)
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["name"] == "Ali Haider"
    assert response.json()["email"] == "alihaider12@gmail.com"
    assert response.json()["username"] == "alihaider1"
    
def test_login():

    response = client.post("/token", data={"username": "alihaider1", "password": "alihaider123"})
    assert response.status_code == 200
    acces_token = response.json()['access_token']

    acces_token_global.append(acces_token)
    


def test_create_todo():
    
    response = client.post(
        "/create-todo/",
        json={"title": "Test Todo", "description": "Testing Todo creation", "completed": False, "due_date": None},
         headers={"Authorization": f"Bearer {acces_token_global[0]}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "Testing Todo creation"
    assert response.json()["completed"] is False
    assert response.json()["due_date"] is None


def test_create_todo():
    # Create a todo for the specific user with ID 1 for testing purposes
    response = client.post(
        "/create-todo/",
        json={"title": "Test Todo", "description": "Testing Todo creation", "completed": False, "due_date": None},
        headers={"Authorization": f"Bearer {acces_token_global[0]}"},
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["title"] == "Test Todo"
    assert response.json()["description"] == "Testing Todo creation"
    assert response.json()["completed"] is False
    assert response.json()["due_date"] is None

def test_read_todo():
    # Get the ID of the todo created in the previous test
    response_create_todo = client.post(
        "/create-todo/",
        json={"title": "Test Todo", "description": "Testing Todo creation", "completed": False, "due_date": None},
        headers={"Authorization": f"Bearer {acces_token_global[0]}"},
    )
    assert response_create_todo.status_code == 200
    todo_id = response_create_todo.json()["id"]

    # Read the todo
    response = client.get(f"/get-todo/{todo_id}", headers={"Authorization": f"Bearer {acces_token_global[0]}"})
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert "title" in response.json()
    assert "description" in response.json()

def test_read_all_todos():
    response = client.get("/get-all-todos/", headers={"Authorization": f"Bearer {acces_token_global[0]}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_todo():
    # Create a todo for the specific user with ID 1 for testing purposes
    response_create_todo = client.post(
        "/create-todo/",
        json={"title": "Test Todo", "description": "Testing Todo creation", "completed": False, "due_date": None},
        headers={"Authorization": f"Bearer {acces_token_global[0]}"},
    )
    assert response_create_todo.status_code == 200
    todo_id = response_create_todo.json()["id"]

    # Update the todo
    response = client.put(
        f"/update-todo/{todo_id}",
        json={"title": "Updated Todo", "description": "Updated description", "completed": True, "due_date": None},
        headers={"Authorization": f"Bearer {acces_token_global[0]}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Todo"
    assert response.json()["description"] == "Updated description"
    assert response.json()["completed"] is True
    assert response.json()["due_date"] == None

def test_delete_todo():
    # Create a todo for the specific user with ID 1 for testing purposes
    response_create_todo = client.post(
        "/create-todo/",
        json={"title": "Test Todo", "description": "Testing Todo creation", "completed": False, "due_date": None},
        headers={"Authorization": f"Bearer {acces_token_global[0]}"},
    )
    assert response_create_todo.status_code == 200
    todo_id = response_create_todo.json()["id"]

    # Delete the todo
    response = client.delete(f"/delete-todo/{todo_id}", headers={"Authorization": f"Bearer {acces_token_global[0]}"})
    assert response.status_code == 200
    assert response.json()["id"] == todo_id
    assert "title" in response.json()
    assert "description" in response.json()

# testing the todo which dont exists
def test_update_non_existent_todo():
    response = client.put(
        "/update-todo/999",
        json={"title": "Updated Todo", "description": "Updated description", "completed": True, "due_date": None},
        headers={"Authorization": f"Bearer {acces_token_global[0]}"}
    )
    assert response.status_code == 404


# testing the unauthorized access
def test_unauthorized_access():
    response = client.get("/get-all-todos/")
    assert response.status_code == 401
    # Add more assertions if needed
