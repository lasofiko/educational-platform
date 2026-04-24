import pytest
from django.contrib.auth.models import User
from django.test import TestCase

from django_app.courses.models import Subject, RoadmapNode
from django_app.progress.models import UserProgress
from django_app.courses.services.roadmap_svc import (
    get_tree,
    get_node_with_status,
    unlock_next_node
)
from django_app.courses.exceptions import NodeLocked, NodeNotFound


class RoadmapServiceTests(TestCase):
    """Тесты для сервиса Roadmap"""

    def setUp(self):
        """Подготовка тестовых данных"""
        # Создаем предмет
        self.subject = Subject.objects.create(
            name="Математика (тестовая)",
            description="Тестовый предмет"
        )

        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )


        self.root1 = RoadmapNode.objects.create(
            subject=self.subject,
            title="Раздел 1",
            node_type="section",
            order=0,
            status="unlocked"
        )

        self.task11 = RoadmapNode.objects.create(
            subject=self.subject,
            parent=self.root1,
            title="Задание 1.1",
            node_type="task",
            order=0,
            status="locked"
        )

        self.task12 = RoadmapNode.objects.create(
            subject=self.subject,
            parent=self.root1,
            title="Задание 1.2",
            node_type="task",
            order=1,
            status="locked"
        )

        self.root2 = RoadmapNode.objects.create(
            subject=self.subject,
            title="Раздел 2",
            node_type="section",
            order=1,
            status="locked"
        )

        self.task21 = RoadmapNode.objects.create(
            subject=self.subject,
            parent=self.root2,
            title="Задание 2.1",
            node_type="task",
            order=0,
            status="locked"
        )

    def test_get_tree_returns_correct_structure(self):
        """Тест 1: get_tree возвращает правильное дерево"""
        tree = get_tree(self.subject.id, self.user)

        self.assertEqual(len(tree), 2)  # Два корневых узла
        self.assertEqual(tree[0]['title'], "Раздел 1")
        self.assertEqual(len(tree[0]['children']), 2)  # Два дочерних узла
        self.assertEqual(tree[0]['children'][0]['title'], "Задание 1.1")
        self.assertEqual(tree[0]['children'][1]['title'], "Задание 1.2")

        self.assertEqual(tree[1]['title'], "Раздел 2")
        self.assertEqual(len(tree[1]['children']), 1)
        self.assertEqual(tree[1]['children'][0]['title'], "Задание 2.1")

    def test_get_node_with_status_first_node_unlocked(self):
        """Первый узел должен быть разблокирован"""
        # Первый корневой узел должен быть разблокирован
        node_info = get_node_with_status(self.root1.id, self.user)
        self.assertEqual(node_info['user_status'], 'unlocked')

    def test_get_node_with_status_locked_raises_exception(self):
        """Тест 2: Открытие locked ноды → NodeLocked"""
        # Задание 1.1 изначально locked, так как нет прогресса
        with self.assertRaises(NodeLocked):
            get_node_with_status(self.task11.id, self.user)

    def test_unlock_next_node_with_sufficient_score(self):
        """Тест 3: Набрал ≥ 70% → следующая разблокирована"""

        # Сначала разблокируем задание 1.1 (оно должно быть unlocked через создание прогресса)
        progress, _ = UserProgress.objects.get_or_create(
            user=self.user,
            node=self.task11,
            defaults={'status': 'unlocked'}
        )

        # Завершаем задание 1.1 с 80% (>=70%)
        result = unlock_next_node(self.user, self.task11.id, 80)

        # Проверяем, что задание 1.1 помечено как complete
        progress.refresh_from_db()
        self.assertEqual(progress.status, 'complete')
        self.assertEqual(progress.score, 80)

        # Проверяем, что задание 1.2 разблокировано
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], self.task12.id)
        self.assertEqual(result['status'], 'unlocked')

        # Проверяем в базе
        task12_progress = UserProgress.objects.get(user=self.user, node=self.task12)
        self.assertEqual(task12_progress.status, 'unlocked')

    def test_unlock_next_node_with_insufficient_score(self):
        """Тест 4: Набрал < 70% → остаётся locked"""

        # Разблокируем задание 1.1
        progress, _ = UserProgress.objects.get_or_create(
            user=self.user,
            node=self.task11,
            defaults={'status': 'unlocked'}
        )

        # Завершаем задание 1.1 с 50% (<70%)
        result = unlock_next_node(self.user, self.task11.id, 50)

        # Проверяем, что задание 1.1 помечено как in_progress (не complete)
        progress.refresh_from_db()
        self.assertEqual(progress.status, 'in_progress')
        self.assertEqual(progress.score, 50)

        # Проверяем, что следующий узел НЕ разблокирован
        self.assertIsNone(result)

        # Проверяем, что прогресса для задания 1.2 нет (или он locked)
        try:
            task12_progress = UserProgress.objects.get(user=self.user, node=self.task12)
            self.assertEqual(task12_progress.status, 'locked')
        except UserProgress.DoesNotExist:
            # Если прогресса нет, это тоже означает locked
            pass

    def test_all_children_completed_unlocks_parent_sibling(self):
        """Тест 5: Все дочерние пройдены → брат родителя разблокирован"""

        # Сначала разблокируем все необходимые узлы
        for node in [self.root1, self.task11, self.task12]:
            UserProgress.objects.get_or_create(
                user=self.user,
                node=node,
                defaults={'status': 'unlocked'}
            )

        # Проходим задание 1.1 с высоким баллом
        unlock_next_node(self.user, self.task11.id, 100)

        # Проходим задание 1.2 с высоким баллом
        result = unlock_next_node(self.user, self.task12.id, 100)

        # Проверяем, что родительский раздел (root1) завершен
        root1_progress = UserProgress.objects.get(user=self.user, node=self.root1)
        self.assertEqual(root1_progress.status, 'complete')

    def tearDown(self):
        """Очистка после тестов"""
        UserProgress.objects.all().delete()
        RoadmapNode.objects.all().delete()
        Subject.objects.all().delete()
        User.objects.all().delete()