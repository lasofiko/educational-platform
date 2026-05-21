import pytest
from services.notifications.services.notification_svc import notification_service

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
    