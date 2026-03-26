from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Иконка")

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ["name"]

    def __str__(self):
        return self.name


class RoadmapNode(models.Model):
    STATUS_CHOICES = [
        ("locked", "Заблокировано"),
        ("unlocked", "Доступно"),
        ("completed", "Пройдено"),
    ]
    NODE_TYPE_CHOICES = [
        ("section", "Раздел"),
        ("task_group", "Группа заданий"),
        ("task", "Конкретное задание"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="nodes",
        verbose_name="Предмет",
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
        verbose_name="Родительская тема",
    )
    title = models.CharField(max_length=300, verbose_name="Название")
    task_number = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Номер задания"
    )
    description = models.TextField(blank=True, verbose_name="Описание")
    node_type = models.CharField(
        max_length=20,
        choices=NODE_TYPE_CHOICES,
        default="section",
        verbose_name="Тип узла",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="locked",
        verbose_name="Статус",
    )

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ["order"]

    def __str__(self):
        if self.task_number:
            return f"Задание {self.task_number}: {self.title}"
        return self.title


class Lesson(models.Model):
    node = models.ForeignKey(
        RoadmapNode,
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name="Тема",
    )
    title = models.CharField(max_length=300, verbose_name="Название")
    content = models.TextField(blank=True, verbose_name="Содержание")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["order"]

    def __str__(self):
        return self.title


class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ("easy", "Лёгкий"),
        ("medium", "Средний"),
        ("hard", "Сложный"),
    ]

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="problems",
        verbose_name="Урок",
    )
    title = models.CharField(max_length=300, verbose_name="Условие")
    description = models.TextField(blank=True, verbose_name="Описание")
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="medium",
        verbose_name="Сложность",
    )
    answer = models.CharField(max_length=500, verbose_name="Ответ")
    solution = models.TextField(blank=True, verbose_name="Решение")
    points = models.PositiveIntegerField(default=1, verbose_name="Баллы")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
        ordering = ["order"]

    def __str__(self):
        return self.title


class Quiz(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="quizzes",
        verbose_name="Урок",
    )
    title = models.CharField(max_length=300, verbose_name="Название")
    passing_score = models.PositiveIntegerField(
        default=70, verbose_name="Проходной балл (%)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.title


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Тест",
    )
    text = models.TextField(verbose_name="Текст вопроса")
    answer = models.CharField(max_length=500, verbose_name="Правильный ответ")
    points = models.PositiveIntegerField(default=1, verbose_name="Баллы")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["order"]

    def __str__(self):
        return self.text
