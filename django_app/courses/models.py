from django.db import models

class Subject(models.Model):
    """
    Модель предмета
    """
    name = models.CharField(max_length=100, verbose_name="Название предмета")
    description = models.TextField(blank=True, verbose_name="Описание")
    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
    def __str__(self):
        return self.name


class RoadmapNode(models.Model):
    """
    Модель узла в дереве тем
    Уровни:
    - Уровень 1: Разделы (Алгебра, Геометрия, Теория вероятностей)
    - Уровень 2: Конкретные подтемы
    - Уровень 3: Номера заданий
    """

    STATUS_CHOICES = [('locked', 'Заблокировано'), ('unlocked', 'Доступно'), ('completed', 'Пройдено')]
    subject = models.ForeignKey( "courses.Subject", on_delete=models.CASCADE, related_name="nodes", verbose_name="Предмет")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children", verbose_name="Родительская тема")

    title = models.CharField(max_length=300, verbose_name="Название")
    task_number = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Номер задания")

    description = models.TextField(blank=True, verbose_name="Описание")

    node_types = [('section', 'Раздел'), ('task_group', 'Группа заданий'), ('task', 'Конкретное задание')]
    node_type = models.CharField(max_length=20, choices=node_types, default='section',verbose_name="Тип узла")
    # cортировка
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='locked', verbose_name="Статус")

    class Meta:
        verbose_name = "Тема"
        verbose_name_plural = "Темы"
        ordering = ['order']

    def __str__(self):
        if self.task_number:
            return f"Задание {self.task_number}: {self.title}"
        return self.title


class Lesson(models.Model):
    """
    Модель урока (содержит теорию и практику)
    """
    node = models.ForeignKey(RoadmapNode, on_delete=models.CASCADE, related_name="lessons", verbose_name="Тема")
    title = models.CharField(max_length=300, verbose_name="Название урока")
    content = models.TextField(blank=True, verbose_name="Содержание (теория)")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['order']

    def __str__(self):
        return self.title


class Task(models.Model):
    """
    Модель задания (конкретная задача)
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="tasks", verbose_name="Урок")
    title = models.CharField(max_length=200, verbose_name="Название задания")
    content = models.TextField(verbose_name="Текст задания")
    answer = models.CharField(max_length=500, blank=True, verbose_name="Ответ")

    difficulty = models.PositiveSmallIntegerField(default=1, verbose_name="Сложность (1-3)")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"
        ordering = ['order']

    def __str__(self):
        return self.title