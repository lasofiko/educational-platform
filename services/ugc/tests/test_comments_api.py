import responses

from services.ugc.tests.conftest import django_exists_url


def _comment_payload(**overrides):
    payload = {
        'target_type': 'lesson',
        'target_id': 1,
        'text': 'Полезный комментарий',
    }
    payload.update(overrides)
    return payload


@responses.activate
def test_post_comment_success(client, auth_headers):
    responses.add(
        responses.GET,
        django_exists_url('lesson', 1),
        json={'exists': True},
        status=200,
    )
    response = client.post(
        '/api/v1/ugc/comments',
        json=_comment_payload(),
        headers=auth_headers(),
    )
    assert response.status_code == 201
    body = response.get_json()
    assert body['text'] == 'Полезный комментарий'
    assert body['status'] == 'active'


def test_post_comment_empty_text_returns_422(client, auth_headers):
    response = client.post(
        '/api/v1/ugc/comments',
        json=_comment_payload(text=''),
        headers=auth_headers(),
    )
    assert response.status_code == 422
    assert 'text' in response.get_json()['error']['fields']
