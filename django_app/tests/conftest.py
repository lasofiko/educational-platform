import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from courses.models import Subject, RoadmapNode, Lesson, Problem, Quiz, QuizQuestion
from progress.models import Enrollment


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpass123')


@pytest.fixture
def subject(db):
    return Subject.objects.create(name='Математика (тестовая)', description='Тест')


@pytest.fixture
def tree(db, subject):
    """root1 (unlocked) → [task11, task12], root2 (locked) → task21"""
    root1 = RoadmapNode.objects.create(
        subject=subject, title='Раздел 1', node_type='section',
        order=0, status='unlocked',
    )
    task11 = RoadmapNode.objects.create(
        subject=subject, parent=root1, title='Задание 1.1',
        node_type='task', order=0, status='locked',
    )
    task12 = RoadmapNode.objects.create(
        subject=subject, parent=root1, title='Задание 1.2',
        node_type='task', order=1, status='locked',
    )
    root2 = RoadmapNode.objects.create(
        subject=subject, title='Раздел 2', node_type='section',
        order=1, status='locked',
    )
    task21 = RoadmapNode.objects.create(
        subject=subject, parent=root2, title='Задание 2.1',
        node_type='task', order=0, status='locked',
    )
    return {'root1': root1, 'task11': task11, 'task12': task12,
            'root2': root2, 'task21': task21}


@pytest.fixture
def lesson(db, tree):
    lesson = Lesson.objects.create(node=tree['task11'], title='Урок 1.1', order=0)
    Problem.objects.create(
        lesson=lesson, title='Задача 1', answer='42',
        difficulty='easy', points=1, order=0,
    )
    return lesson


@pytest.fixture
def quiz(db, lesson):
    quiz = Quiz.objects.create(lesson=lesson, title='Тест 1', passing_score=70)
    QuizQuestion.objects.create(quiz=quiz, text='2+2=?', answer='4', points=1, order=0)
    QuizQuestion.objects.create(quiz=quiz, text='3+3=?', answer='6', points=1, order=1)
    return quiz


@pytest.fixture
def enrolled_user(db, user, subject):
    Enrollment.objects.create(user=user, subject=subject)
    return user


@pytest.fixture
def api_client(db, user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
