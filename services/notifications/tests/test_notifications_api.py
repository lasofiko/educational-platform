from services.notifications.services.notification_svc import notification_service

import jwt
import pytest

async def create_notification(client, user_id, title="test"):
    return await client.post(
        "/api/v1/notifications",
        json={
            "user_id": user_id,
            "title": title,
            "body": "test body",
            "notification_type": "info",
        },
    )

@pytest.mark.asyncio
async def test_create_notification_success(client):
    response = await client.post(
        '/api/v1/notifications',
        json={
            'user_id': 1,
            'title': 'Тема разблокирована',
            'body': 'Вы открыли новую тему в курсе.',
            'notification_type': 'node_unlocked',
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data['id'] >= 1
    assert data['user_id'] == 1
    assert data['title'] == 'Тема разблокирована'
    assert data['body'] == 'Вы открыли новую тему в курсе.'
    assert data['notification_type'] == 'node_unlocked'
    assert data['status'] == 'pending'
    assert 'created_at' in data


@pytest.mark.asyncio
async def test_create_notification_invalid_returns_422(client):
    response = await client.post(
        '/api/v1/notifications',
        json={
            'user_id': 0,
            'title': '',
            'body': '',
        },
    )
    assert response.status_code == 422
    detail = response.json()['detail']
    assert isinstance(detail, list)
    loc_fields = {err['loc'][-1] for err in detail}
    assert 'user_id' in loc_fields
    assert 'title' in loc_fields
    assert 'body' in loc_fields


@pytest.mark.asyncio
async def test_create_notification_schedule_dispatch(client, monkeypatch):
    called_with = []
    
    async def fake_dispatch(notification_id):
        called_with.append(notification_id)
        
    monkeypatch.setattr(notification_service, "dispatch", fake_dispatch)

    response = await client.post(
        '/api/v1/notifications',
        json={
            'user_id': 1,
            'title': 'Тема разблокирована',
            'body': 'Вы открыли новую тему в курсе.',
            'notification_type': 'node_unlocked',
        },
    )

    assert len(called_with) == 1
    assert response.json()["id"] == called_with[0]

@pytest.mark.asyncio
async def test_handle_node_unlocked_success(client):
    response = await client.post(
        '/api/v1/notifications/node-unlocked',
        json={
            'user_id': 1,
            'node_id': 4,
            'node_title': "Алгебра"
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data['id'] >= 1
    assert data['user_id'] == 1
    assert data['title'] == "Тема разблокирована"
    assert data['status'] == "pending"
    assert data['body'] == f"Вы открыли тему: «Алгебра»"
    assert data['notification_type'] == "node_unlocked"

@pytest.mark.asyncio
async def test_list_notifications_no_token(client):
    response = await client.get(
        '/api/v1/notifications/me'
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_list_notifications_bad_token(client, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "very-very-secret-secret")
    response = await client.get(
        '/api/v1/notifications/me'
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_list_notifications_correct_user(client, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    token = jwt.encode({"user_id": 1}, "test-secret", algorithm="HS256")

    response = await client.get(
        '/api/v1/notifications/me',
        headers={"Authorization": f"Bearer {token}"}
        )

    notifications_num = len(response.json()) + 2

    await create_notification(client, user_id=1)
    await create_notification(client, user_id=1)
    await create_notification(client, user_id=2)


    response = await client.get(
        '/api/v1/notifications/me',
        headers={"Authorization": f"Bearer {token}"}
    )


    assert response.status_code == 200

    data = response.json()

    assert all(item["user_id"] == 1 for item in data)
    assert len(data) == notifications_num

@pytest.mark.asyncio
async def test_list_notifications_pagination(client, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "test-secret")
    token = jwt.encode({"user_id": 1}, "test-secret", algorithm="HS256")

    for _ in range(5):
        await create_notification(client, user_id=1)
    
    response = await client.get(
        '/api/v1/notifications/me?limit=2&offset=1',
        headers={"Authorization": f"Bearer {token}"}
        )

    data = response.json()

    assert len(data) == 2
