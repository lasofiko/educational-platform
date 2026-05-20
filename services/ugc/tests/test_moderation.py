import responses

from services.ugc.tests.conftest import django_exists_url


@responses.activate
def test_moderate_review_success(client, auth_headers):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 10),
        json={'exists': True},
        status=200,
    )
    create_resp = client.post(
        '/api/v1/ugc/reviews',
        json={
            'target_type': 'lesson',
            'target_id': 10,
            'rating': 4,
            'text': 'На модерацию',
        },
        headers=auth_headers(user_id=5),
    )
    review_id = create_resp.get_json()['id']

    response = client.post(
        f'/api/v1/ugc/admin/review/{review_id}/moderate',
        json={'status': 'hidden'},
        headers=auth_headers(user_id=1, is_staff=True),
    )
    assert response.status_code == 200
    assert response.get_json()['status'] == 'hidden'


@responses.activate
def test_moderate_non_staff_returns_403(client, auth_headers):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 11),
        json={'exists': True},
        status=200,
    )
    create_resp = client.post(
        '/api/v1/ugc/reviews',
        json={
            'target_type': 'lesson',
            'target_id': 11,
            'rating': 3,
            'text': 'Тест',
        },
        headers=auth_headers(user_id=6),
    )
    review_id = create_resp.get_json()['id']

    response = client.post(
        f'/api/v1/ugc/admin/review/{review_id}/moderate',
        json={'status': 'hidden'},
        headers=auth_headers(user_id=6, is_staff=False),
    )
    assert response.status_code == 403


def test_moderate_invalid_status_returns_422(client, auth_headers):
    response = client.post(
        '/api/v1/ugc/admin/review/1/moderate',
        json={'status': 'banned'},
        headers=auth_headers(is_staff=True),
    )
    assert response.status_code == 422
    assert 'status' in response.get_json()['error']['fields']
