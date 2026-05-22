import pytest
from django.test import TestCase
from django.contrib.auth.models import User

from courses.services.lesson_svc import (
    get_lesson_with_problems,
    get_lessons_for_node,
    get_problem_with_answer,
)
from courses.exceptions import LessonNotFound, NodeLocked
from progress.models import UserProgress
#
class TestGetLessonWithProblems(TestCase):
    """Тесты для get_lesson_with_problems(lesson_id, user)"""
    def setUp(self):

        from courses.models import Subject, RoadmapNode, Lesson, Problem
        self.subject = Subject.objects.create(name="Тестовый предмет")
        self.user = User.objects.create_user(username="testuser", password="12345")

        self.root_node = RoadmapNode.objects.create(
            subject=self.subject,
            title="Корневой узел",
            node_type="section",
            order=0,
            status="unlocked",
            parent=None
        )

        self.lesson = Lesson.objects.create(
            node=self.root_node,
            title="Тестовый урок",
            order=0
        )

        self.problem = Problem.objects.create(
            lesson=self.lesson,
            title="Тестовая задача",
            answer="42",
            solution="Ответ 42",
            points=1,
            order=0
        )

    def test_get_lesson_with_problems_success(self):
        """Успешное получение урока с задачами"""
        result = get_lesson_with_problems(self.lesson.id, self.user)

        self.assertEqual(result['id'], self.lesson.id)
        self.assertEqual(result['title'], self.lesson.title)
        self.assertEqual(len(result['problems']), 1)
        self.assertEqual(result['problems'][0]['title'], 'Тестовая задача')

    def test_get_lesson_with_problems_lesson_not_found(self):
        """LessonNotFound при запросе несуществующего урока"""
        with self.assertRaises(LessonNotFound):
            get_lesson_with_problems(99999, self.user)

    def test_get_lesson_with_problems_node_locked(self):
        """NodeLocked если у пользователя статус 'locked' для ноды"""
        # Создаем прогресс со статусом locked
        UserProgress.objects.create(
            user=self.user,
            node=self.root_node,
            status='locked',
            score=0
        )

        with self.assertRaises(NodeLocked):
            get_lesson_with_problems(self.lesson.id, self.user)


class TestGetLessonsForNode(TestCase):
    """Тесты для get_lessons_for_node(node_id)"""

    def setUp(self):
        from courses.models import Subject, RoadmapNode, Lesson

        self.subject = Subject.objects.create(name="Тестовый предмет")
        self.node = RoadmapNode.objects.create(
            subject=self.subject,
            title="Тестовый узел",
            node_type="section",
            order=0
        )
        self.lesson1 = Lesson.objects.create(node=self.node, title="Урок 1", order=0)
        self.lesson2 = Lesson.objects.create(node=self.node, title="Урок 2", order=1)

    def test_get_lessons_for_node_success(self):
        """Успешное получение списка уроков для ноды"""
        result = get_lessons_for_node(self.node.id)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], 'Урок 1')
        self.assertEqual(result[1]['title'], 'Урок 2')

    def test_get_lessons_for_node_empty(self):
        """Возвращает пустой список, если у ноды нет уроков"""
        from courses.models import RoadmapNode

        empty_node = RoadmapNode.objects.create(
            subject=self.subject,
            title="Пустой узел",
            node_type="section",
            order=2
        )
        result = get_lessons_for_node(empty_node.id)

        self.assertEqual(result, [])


class TestGetProblemWithAnswer(TestCase):
    """Тесты для get_problem_with_answer(problem_id, user)"""

    def setUp(self):
        from courses.models import Subject, RoadmapNode, Lesson, Problem

        self.subject = Subject.objects.create(name="Тестовый предмет")
        self.user = User.objects.create_user(username="testuser2", password="12345")

        self.node = RoadmapNode.objects.create(
            subject=self.subject,
            title="Тестовый узел",
            node_type="section",
            order=0,
            status="unlocked",
            parent=None
        )
        self.lesson = Lesson.objects.create(node=self.node, title="Тестовый урок", order=0)
        self.problem = Problem.objects.create(
            lesson=self.lesson,
            title="Тестовая задача",
            answer="secret_answer",
            solution="secret_solution",
            points=10,
            order=0
        )

    def test_get_problem_with_answer_success(self):
        """Успешное получение задачи с ответом и решением"""
        result = get_problem_with_answer(self.problem.id, self.user)

        self.assertEqual(result['id'], self.problem.id)
        self.assertEqual(result['answer'], 'secret_answer')
        self.assertEqual(result['solution'], 'secret_solution')
        self.assertEqual(result['points'], 10)

    def test_get_problem_with_answer_not_found(self):
        """LessonNotFound при запросе несуществующей задачи"""
        with self.assertRaises(LessonNotFound):
            get_problem_with_answer(99999, self.user)

    def test_get_problem_with_answer_node_locked(self):
        """NodeLocked если нода заблокирована"""
        UserProgress.objects.create(
            user=self.user,
            node=self.node,
            status='locked',
            score=0
        )

        with self.assertRaises(NodeLocked):
            get_problem_with_answer(self.problem.id, self.user)