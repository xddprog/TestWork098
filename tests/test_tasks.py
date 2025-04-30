import asyncio
from datetime import datetime, timedelta, timezone
import pytest


@pytest.fixture
async def auth_headers(async_client):
    await async_client.post("/auth/register", json={
        "name": "Task User",
        "email": "task@example.com",
        "password": "taskpass"
    })
    login_resp = await async_client.post("/auth/login", json={
        "email": "task@example.com",
        "password": "taskpass"
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_create_task_valid(async_client, auth_headers):
    response = await async_client.post("/tasks", json={
        "title": "Important Task",
        "description": "Top priority work",
        "status": "pending",
        "priority": 10
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Important Task"
    assert data["priority"] == 10
    assert data["status"] in ["pending", "todo"]


@pytest.mark.asyncio
async def test_create_task_invalid_priority(async_client, auth_headers):
    response = await async_client.post("/tasks", json={
        "title": "Invalid Priority",
        "description": "Should fail",
        "status": "todo",
        "priority": "high"
    }, headers=auth_headers)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_tasks_with_filters(async_client, auth_headers):
    response = await async_client.get("/tasks", params={
        "status": "pending",
        "priority": 2
    }, headers=auth_headers)

    assert response.status_code == 200
    tasks = response.json()
    for task in tasks:
        assert task["status"] == "todo"
        assert task["priority"] == 2

@pytest.mark.asyncio
async def test_get_tasks_with_date_from(async_client, auth_headers):
    await async_client.post("/tasks", json={
        "title": "Old Task",
        "description": "Created earlier",
        "status": "pending",
        "priority": 1
    }, headers=auth_headers)

    await asyncio.sleep(1)

    await async_client.post("/tasks", json={
        "title": "New Task",
        "description": "Created later",
        "status": "todo",
        "priority": 2
    }, headers=auth_headers)

    date_from = (datetime.now() - timedelta(seconds=0.5)).isoformat()

    response = await async_client.get("/tasks", params={"date_from": date_from}, headers=auth_headers)
    assert response.status_code == 200
    tasks = response.json()
    for task in tasks:
        created_at = task["created_at"]
        assert created_at >= date_from


@pytest.mark.asyncio
async def test_get_tasks_with_date_to(async_client, auth_headers):
    await async_client.post("/tasks", json={
        "title": "Early Task",
        "description": "Created first",
        "status": "todo",
        "priority": 1
    }, headers=auth_headers)

    await asyncio.sleep(1)

    await async_client.post("/tasks", json={
        "title": "Late Task",
        "description": "Created second",
        "status": "todo",
        "priority": 2
    }, headers=auth_headers)

    date_to = (datetime.now() - timedelta(seconds=0.5)).isoformat()

    response = await async_client.get("/tasks", params={"date_to": date_to}, headers=auth_headers)
    assert response.status_code == 200
    tasks = response.json()
    for task in tasks:
        created_at = task["created_at"]
        assert created_at <= date_to


@pytest.mark.asyncio
async def test_search_tasks(async_client, auth_headers):
    await async_client.post("/tasks", json={
        "title": "Search me",
        "description": "Contains magicword",
        "status": "pending",
        "priority": 3
    }, headers=auth_headers)

    response = await async_client.get("/tasks/search?q=magicword", headers=auth_headers)
    assert response.status_code == 200
    results = response.json()
    assert any("magicword" in task["description"] for task in results)


@pytest.mark.asyncio
async def test_create_task_without_token(async_client):
    response = await async_client.post("/tasks", json={
        "title": "Task Without Auth",
        "description": "Should fail",
        "priority": 1
    })
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_task_invalid_id(async_client, auth_headers):
    response = await async_client.put(
        "/tasks/9999", 
        json={
            "title": "Updated",
            "description": "No such task"
        }, 
        headers=auth_headers
    )

    assert response.status_code == 404
