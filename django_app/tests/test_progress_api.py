import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_enrollment_list_empty(api_client):
    response = api_client.get('/api/v1/progress/enrollments/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_enroll_creates_enrollment(api_client, subject):
    response = api_client.post(
        '/api/v1/progress/enrollments/', {'subject': subject.id}, format='json'
    )
    assert response.status_code == 201
    assert response.data['subject'] == subject.id


@pytest.mark.django_db
def test_enroll_twice_returns_409(api_client, enrolled_user, subject):
    response = api_client.post(
        '/api/v1/progress/enrollments/', {'subject': subject.id}, format='json'
    )
    assert response.status_code == 409
    assert response.data['error']['code'] == 'already_enrolled'


@pytest.mark.django_db
def test_enroll_unknown_subject(api_client):
    response = api_client.post(
        '/api/v1/progress/enrollments/', {'subject': 99999}, format='json'
    )
    assert response.status_code in (400, 404)


@pytest.mark.django_db
def test_my_progress_list(api_client):
    response = api_client.get('/api/v1/progress/my/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_stats_requires_subject_id(api_client):
    response = api_client.get('/api/v1/progress/my/stats/')
    assert response.status_code == 400


@pytest.mark.django_db
def test_stats_zero_for_new_user(api_client, subject):
    response = api_client.get(f'/api/v1/progress/my/stats/?subject_id={subject.id}')
    assert response.status_code == 200
    assert response.data['nodes_completed'] == 0


@pytest.mark.django_db
def test_submit_correct_answer(api_client, lesson):
    problem = lesson.problems.first()
    response = api_client.post(
        f'/api/v1/progress/problems/{problem.id}/submit/',
        {'problem_id': problem.id, 'answer': '42'},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['correct'] is True
    assert response.data['points'] == 1


@pytest.mark.django_db
def test_submit_wrong_answer(api_client, lesson):
    problem = lesson.problems.first()
    response = api_client.post(
        f'/api/v1/progress/problems/{problem.id}/submit/',
        {'problem_id': problem.id, 'answer': 'wrong'},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['correct'] is False


@pytest.mark.django_db
def test_submit_quiz_passing(api_client, quiz):
    response = api_client.post(
        f'/api/v1/progress/quizzes/{quiz.id}/submit/',
        {'quiz_id': quiz.id, 'answers': {str(q.id): q.answer for q in quiz.questions.all()}},
        format='json',
    )
    assert response.status_code == 200
    assert response.data['passed'] is True


@pytest.mark.django_db
def test_submit_quiz_failing(api_client, quiz):
    response = api_client.post(
        f'/api/v1/progress/quizzes/{quiz.id}/submit/',
        {'quiz_id': quiz.id, 'answers': {str(q.id): 'x' for q in quiz.questions.all()}},
        format='json',
    )
    assert response.status_code == 400
    assert response.data['error']['code'] == 'quiz_failed'


@pytest.mark.django_db
def test_unauthenticated_returns_401():
    client = APIClient()
    response = client.get('/api/v1/progress/enrollments/')
    assert response.status_code == 401
