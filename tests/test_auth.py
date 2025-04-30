from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_register(async_client: AsyncClient):
    response = await async_client.post("/auth/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_login(async_client: AsyncClient):
    response = await async_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    return data

@pytest.mark.asyncio
async def test_refresh_token(async_client: AsyncClient):
    login_response = await async_client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "securepassword123"
    })
    refresh_token = login_response.json()["refresh_token"]

    response = await async_client.post("/auth/refresh", params={
        "refresh_token": refresh_token
    })

    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_register_existing_user(async_client: AsyncClient):
    await async_client.post("/auth/register", json={
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "pass123"
    })

    response = await async_client.post("/auth/register", json={
        "name": "Duplicate User",
        "email": "duplicate@example.com",
        "password": "pass123"
    })

    assert response.status_code == 403
    assert response.json()["detail"] == "User is already registered"

@pytest.mark.asyncio
async def test_login_nonexistent_user(async_client: AsyncClient):
    response = await async_client.post("/auth/login", json={
        "email": "nosuchuser@example.com",
        "password": "whatever"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "User with this email not found"

@pytest.mark.asyncio
async def test_login_invalid_password(async_client: AsyncClient):
    await async_client.post("/auth/register", json={
        "name": "Wrong Pass",
        "email": "wrongpass@example.com",
        "password": "correctpass"
    })

    response = await async_client.post("/auth/login", json={
        "email": "wrongpass@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_access_protected_without_token(async_client: AsyncClient):
    response = await async_client.get("/tasks")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_refresh_with_invalid_token(async_client: AsyncClient):
    response = await async_client.post("/auth/refresh", params={
        "refresh_token": "invalid_token"
    })
    assert response.status_code == 401
