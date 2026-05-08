import pytest
from rest_framework.test import APIClient

from courses.models import Lesson, Problem


def _payload_rows(response):
    data = response.data
    if isinstance(data, dict) and 'results' in data:
        return data['results']
    return data


def _assert_tree_nested_roots(nodes, subject_id):
    assert isinstance(nodes, list)
    for root in nodes:
        assert root['parent_id'] is None
        assert root['subject_id'] == subject_id
        assert 'children' in root
        assert isinstance(root['children'], list)
        assert 'user_status' in root
        _walk_tree_children(root['children'], parent_id=root['id'], subject_id=subject_id)


def _walk_tree_children(children, parent_id, subject_id):
    for node in children:
        assert node['parent_id'] == parent_id
        assert node['subject_id'] == subject_id
        assert 'children' in node
        assert isinstance(node['children'], list)
        assert 'user_status' in node
        _walk_tree_children(node['children'], parent_id=node['id'], subject_id=subject_id)


@pytest.mark.django_db
def test_subjects_list_returns_200_and_pagination(api_client, subject):
    response = api_client.get('/api/v1/courses/subjects/')
    assert response.status_code == 200
    body = response.data
    assert 'count' in body
    assert 'results' in body
    assert body['count'] >= 1
    rows = body['results']
    assert len(rows) >= 1
    ids = [row['id'] for row in rows]
    assert subject.id in ids


@pytest.mark.django_db
def test_subjects_retrieve(api_client, subject):
    response = api_client.get(f'/api/v1/courses/subjects/{subject.id}/')
    assert response.status_code == 200
    assert response.data['id'] == subject.id


@pytest.mark.django_db
def test_subjects_list_allow_any_unauthenticated_not_401(subject):
    client = APIClient()
    response = client.get('/api/v1/courses/subjects/')
    assert response.status_code == 200
    assert 'results' in response.data
    ids = [row['id'] for row in response.data['results']]
    assert subject.id in ids


@pytest.mark.django_db
def test_roadmap_list_nested_trees_roots_without_parent(api_client, subject, tree):
    assert tree['root1'].subject_id == subject.id
    response = api_client.get(f'/api/v1/courses/roadmap/?subject_id={subject.id}')
    assert response.status_code == 200
    data = response.data
    assert isinstance(data, list)
    assert len(data) == 2
    root_ids = {n['id'] for n in data if n['parent_id'] is None}
    assert root_ids == {tree['root1'].id, tree['root2'].id}
    _assert_tree_nested_roots(data, subject.id)


@pytest.mark.django_db
def test_roadmap_retrieve_detail_includes_user_status(api_client, tree):
    root_id = tree['root1'].id
    response = api_client.get(f'/api/v1/courses/roadmap/{root_id}/')
    assert response.status_code == 200
    assert 'user_status' in response.data
    assert response.data['id'] == root_id


@pytest.mark.django_db
def test_roadmap_retrieve_locked_returns_403(api_client, tree):
    locked_id = tree['task21'].id
    response = api_client.get(f'/api/v1/courses/roadmap/{locked_id}/')
    assert response.status_code == 403
    assert response.data['error']['code'] == 'node_locked'


@pytest.mark.django_db
def test_roadmap_retrieve_not_found_returns_404(api_client):
    response = api_client.get('/api/v1/courses/roadmap/9999/')
    assert response.status_code == 404
    assert response.data['error']['code'] == 'node_not_found'


@pytest.mark.django_db
def test_roadmap_progress_unauthenticated_returns_401(tree):
    client = APIClient()
    response = client.get(
        f'/api/v1/courses/roadmap/{tree["root1"].id}/progress/'
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_roadmap_progress_authenticated_returns_status_score_completed_at(
    api_client, tree
):
    node_id = tree['root1'].id
    response = api_client.get(f'/api/v1/courses/roadmap/{node_id}/progress/')
    assert response.status_code == 200
    body = response.data
    assert str(body['node_id']) == str(node_id)
    assert 'status' in body
    assert 'score' in body
    assert 'completed_at' in body


@pytest.mark.django_db
def test_lesson_retrieve_ok_includes_node_and_problems(api_client, tree):
    root1 = tree['root1']
    lesson = Lesson.objects.create(node=root1, title='Урок (корень)', order=0)
    Problem.objects.create(
        lesson=lesson,
        title='Задача А',
        answer='42',
        difficulty='easy',
        points=2,
        order=0,
    )
    response = api_client.get(f'/api/v1/courses/lessons/{lesson.id}/')
    assert response.status_code == 200
    data = response.data
    assert data['id'] == lesson.id
    assert data['title'] == 'Урок (корень)'
    assert data['node']['id'] == root1.id
    assert data['node']['title'] == root1.title
    assert len(data['problems']) == 1
    prob = data['problems'][0]
    assert prob['title'] == 'Задача А'
    assert prob['difficulty'] == 'easy'
    assert prob['points'] == 2
    assert 'answer' not in prob


@pytest.mark.django_db
def test_lesson_retrieve_locked_node_returns_403(api_client, lesson):
    response = api_client.get(f'/api/v1/courses/lessons/{lesson.id}/')
    assert response.status_code == 403
    assert response.data['error']['code'] == 'node_locked'


@pytest.mark.django_db
def test_lesson_retrieve_not_found_returns_404(api_client):
    response = api_client.get('/api/v1/courses/lessons/9999/')
    assert response.status_code == 404
    assert response.data['error']['code'] == 'lesson_not_found'


@pytest.mark.django_db
def test_lessons_by_node_returns_lessons_for_node(api_client, tree, lesson):
    response = api_client.get(
        f'/api/v1/courses/lessons/by-node/{tree["task11"].id}/'
    )
    assert response.status_code == 200
    rows = response.data
    assert isinstance(rows, list)
    match = next(r for r in rows if r['id'] == lesson.id)
    assert match['title'] == lesson.title
    assert 'order' in match and 'created_at' in match


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
