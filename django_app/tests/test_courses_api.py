import pytest
from rest_framework.test import APIClient

from courses.models import Problem


def _payload_rows(response):
    data = response.data
    if isinstance(data, dict) and 'results' in data:
        return data['results']
    return data


@pytest.mark.django_db
def test_subjects_list(api_client, subject):
    response = api_client.get('/api/v1/courses/subjects/')
    assert response.status_code == 200
    rows = _payload_rows(response)
    assert len(rows) >= 1
    ids = [row['id'] for row in rows]
    assert subject.id in ids


@pytest.mark.django_db
def test_subjects_retrieve(api_client, subject):
    response = api_client.get(f'/api/v1/courses/subjects/{subject.id}/')
    assert response.status_code == 200
    assert response.data['id'] == subject.id


@pytest.mark.django_db
def test_roadmap_list(api_client, subject, tree):
    assert tree['root1'].subject_id == subject.id
    response = api_client.get(f'/api/v1/courses/roadmap/?subject_id={subject.id}')
    assert response.status_code == 200
    assert isinstance(response.data, list)
    assert len(response.data) >= 1


@pytest.mark.django_db
def test_roadmap_retrieve_locked_returns_403(api_client, tree):
    locked_id = tree['task21'].id
    response = api_client.get(f'/api/v1/courses/roadmap/{locked_id}/')
    assert response.status_code == 403
    assert response.data['error']['code'] == 'node_locked'


@pytest.mark.django_db
def test_roadmap_retrieve_not_found_returns_404(api_client):
    response = api_client.get('/api/v1/courses/roadmap/999999/')
    assert response.status_code == 404
    assert response.data['error']['code'] == 'node_not_found'


@pytest.mark.django_db
def test_lesson_retrieve_locked_node_returns_403(api_client, lesson):
    response = api_client.get(f'/api/v1/courses/lessons/{lesson.id}/')
    assert response.status_code == 403
    assert response.data['error']['code'] == 'node_locked'


@pytest.mark.django_db
def test_lessons_by_node(api_client, tree, lesson):
    response = api_client.get(
        f'/api/v1/courses/lessons/by-node/{tree["task11"].id}/'
    )
    assert response.status_code == 200
    ids = [row['id'] for row in response.data]
    assert lesson.id in ids


@pytest.mark.django_db
def test_problems_filter_by_difficulty(api_client, lesson):
    Problem.objects.create(
        lesson=lesson,
        title='Задача medium',
        answer='1',
        difficulty='medium',
        points=1,
        order=1,
    )
    response = api_client.get('/api/v1/courses/problems/?difficulty=easy')
    assert response.status_code == 200
    for row in _payload_rows(response):
        assert row['difficulty'] == 'easy'


@pytest.mark.django_db
def test_problems_filter_by_lesson(api_client, lesson):
    response = api_client.get(
        f'/api/v1/courses/problems/?lesson={lesson.id}'
    )
    assert response.status_code == 200
    rows = _payload_rows(response)
    assert len(rows) >= 1
    for row in rows:
        assert row['lesson'] == lesson.id


@pytest.mark.django_db
def test_problems_list_excludes_answer_and_solution(api_client, lesson):
    response = api_client.get('/api/v1/courses/problems/')
    assert response.status_code == 200
    rows = _payload_rows(response)
    assert len(rows) >= 1
    for row in rows:
        assert 'answer' not in row
        assert 'solution' not in row


@pytest.mark.django_db
def test_problem_retrieve_includes_answer_and_solution(api_client, lesson):
    problem = lesson.problems.first()
    response = api_client.get(f'/api/v1/courses/problems/{problem.id}/')
    assert response.status_code == 200
    assert response.data['answer'] == '42'
    assert 'solution' in response.data


@pytest.mark.django_db
def test_quizzes_list(api_client, quiz):
    response = api_client.get('/api/v1/courses/quizzes/')
    assert response.status_code == 200
    rows = _payload_rows(response)
    ids = [row['id'] for row in rows]
    assert quiz.id in ids


@pytest.mark.django_db
def test_quizzes_list_excludes_question_answers(api_client, quiz):
    response = api_client.get('/api/v1/courses/quizzes/')
    assert response.status_code == 200
    quiz_row = next(row for row in _payload_rows(response) if row['id'] == quiz.id)
    for question in quiz_row['questions']:
        assert 'answer' not in question
