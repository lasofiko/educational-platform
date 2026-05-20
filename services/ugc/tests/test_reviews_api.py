import responses

from services.ugc.tests.conftest import django_exists_url
from services.ugc.models import Review, db


def _review_payload(**overrides):
    payload = {
        'target_type': 'lesson',
        'target_id': 1,
        'rating': 5,
        'text': 'Отличный урок',
    }
    payload.update(overrides)
    return payload


@responses.activate
def test_post_review_success(client, auth_headers):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 1),
        json={'exists': True},
        status=200,
    )
    response = client.post(
        '/api/v1/ugc/reviews',
        json=_review_payload(),
        headers=auth_headers(),
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body['rating'] == 5
    assert body['target_type'] == 'lesson'
    assert body['status'] == 'active'


@responses.activate
def test_post_review_duplicate_returns_409(client, auth_headers):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 1),
        json={'exists': True},
        status=200,
    )
    headers = auth_headers(user_id=42)
    payload = _review_payload()
    first = client.post('/api/v1/ugc/reviews', json=payload, headers=headers)
    assert first.status_code == 201

    second = client.post('/api/v1/ugc/reviews', json=payload, headers=headers)
    assert second.status_code == 409
    assert second.get_json()['error']['code'] == 'duplicate_review'


def test_post_review_rating_zero_returns_422(client, auth_headers):
    response = client.post(
        '/api/v1/ugc/reviews',
        json=_review_payload(rating=0),
        headers=auth_headers(),
    )
    assert response.status_code == 422
    assert 'rating' in response.get_json()['error']['fields']


def test_post_review_invalid_target_type_returns_422(client, auth_headers):
    response = client.post(
        '/api/v1/ugc/reviews',
        json=_review_payload(target_type='course'),
        headers=auth_headers(),
    )
    assert response.status_code == 422
    assert 'target_type' in response.get_json()['error']['fields']


@responses.activate
def test_post_review_target_not_found_returns_404(client, auth_headers):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 999),
        status=404,
    )
    response = client.post(
        '/api/v1/ugc/reviews',
        json=_review_payload(target_id=999),
        headers=auth_headers(),
    )
    assert response.status_code == 404
    assert response.get_json()['error']['code'] == 'target_not_found'


@responses.activate
def test_post_review_without_token_returns_401(client):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 1),
        json={'exists': True},
        status=200,
    )
    response = client.post('/api/v1/ugc/reviews', json=_review_payload())
    assert response.status_code == 401


@responses.activate
def test_get_reviews_excludes_hidden(client, auth_headers, app):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 2),
        json={'exists': True},
        status=200,
    )
    create_resp = client.post(
        '/api/v1/ugc/reviews',
        json=_review_payload(target_id=2, text='Будет скрыт'),
        headers=auth_headers(user_id=7),
    )
    assert create_resp.status_code == 201
    review_id = create_resp.get_json()['id']

    with app.app_context():
        review = db.session.get(Review, review_id)
        review.status = 'hidden'
        db.session.commit()

    list_resp = client.get('/api/v1/ugc/reviews?target_type=lesson&target_id=2')
    assert list_resp.status_code == 200
    results = list_resp.get_json()['results']
    assert all(item['id'] != review_id for item in results)


@responses.activate
def test_get_reviews_returns_visible_items(client, auth_headers):
    responses.add(
        responses.GET,
        django_exists_url('subject', 3),
        json={'exists': True},
        status=200,
    )
    client.post(
        '/api/v1/ugc/reviews',
        json=_review_payload(target_type='subject', target_id=3),
        headers=auth_headers(user_id=3),
    )
    response = client.get('/api/v1/ugc/reviews?target_type=subject&target_id=3')
    assert response.status_code == 200
    assert len(response.get_json()['results']) == 1
