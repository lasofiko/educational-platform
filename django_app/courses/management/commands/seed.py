from django.core.management.base import BaseCommand
from django.db import transaction
from courses.models import Subject, RoadmapNode, Lesson, Task

roadmap_data = [
    {
        "title": "Алгебра",
        "description": "Алгебраические задачи ЕГЭ по математике (профильный уровень)",
        "children": [
            {
                "title": "Числа и вычисления",
                "description": "Действительные числа, проценты, пропорции, корни, степени",
                "children": [
                    {
                        "title": "Задание 9",
                        "description": "Задачи с прикладным содержанием",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 9.1",
                                "content": "",
                                "answer": "",
                                "difficulty": 1
                            },
                        ]
                    }
                ]
            },
            {
                "title": "Векторы",
                "description": "Векторы на плоскости и в пространстве",
                "children": [
                    {
                        "title": "Задание 2",
                        "description": "Действия с векторами: скалярное произведение, координаты векторов, длина вектора",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 2.1",
                                "content": "Найдите скалярное произведение векторов a(1, 2) и b(3, 4)",
                                "answer": "1×3 + 2×4 = 3 + 8 = 11",
                                "difficulty": 1
                            },
                        ]
                    }
                ]
            },
            {
                "title": "Уравнения и преобразования выражений",
                "description": "Решение уравнений различных типов и преобразование выражений",
                "children": [
                    {
                        "title": "Задание 6",
                        "description": "Простейшие уравнения",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 6.1",
                                "content": "",
                                "answer": "",
                                "difficulty": 1
                            }
                        ]
                    },
                    {
                        "title": "Задание 7",
                        "description": "Вычисления и преобразования",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 7.1",
                                "content": "",
                                "answer": "",
                                "difficulty": 1
                            }
                        ]
                    },
                    {
                        "title": "Задание 13",
                        "description": "Тригонометрические уравнения",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 13.1",
                                "content": "Решите уравнение: sin²x + sin x = 0",
                                "answer": "x = πn, x = -π/2 + 2πn, x = 3π/2 + 2πn, n ∈ Z",
                                "difficulty": 2
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Неравенства",
                "description": "Решение неравенств различных типов",
                "children": [
                    {
                        "title": "Задание 13: Логарифмические неравенства",
                        "description": "Решение логарифмических неравенств",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 13.1",
                                "content": "Решите неравенство: log₂(x + 3) < 2",
                                "answer": "-3 < x < 1",
                                "difficulty": 2
                            }
                        ]
                    },
                    {
                        "title": "Задание 15",
                        "description": "Решение рациональных, иррациональных и показательных неравенств",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 15.1",
                                "content": "Решите неравенство: x² - 4x + 3 > 0",
                                "answer": "x < 1 или x > 3",
                                "difficulty": 1
                            },
                            {
                                "title": "Задание 15.2",
                                "content": "Решите неравенство: 2ˣ > 8",
                                "answer": "x > 3",
                                "difficulty": 1
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Функции и графики",
                "description": "Исследование функций и работа с графиками",
                "children": [
                    {
                        "title": "Задание 11",
                        "description": "Чтение графиков, определение свойств функций по графику",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 11.2",
                                "content": "По графику функции определите промежутки возрастания",
                                "answer": "Зависит от графика",
                                "difficulty": 1
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Производная и исследование функций",
                "description": "Применение производной для исследования функций",
                "children": [
                    {
                        "title": "Задание 8",
                        "description": "Точки экстремума, наибольшее и наименьшее значение",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 8.1",
                                "content": "Найдите точки экстремума функции f(x) = x³ - 3x²",
                                "answer": "x = 0 (max), x = 2 (min)",
                                "difficulty": 1
                            }
                        ]
                    },
                    {
                        "title": "Задание 12: Исследование функций",
                        "description": "Полное исследование функций с помощью производной",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 12.1",
                                "content": "Найдите промежутки возрастания и убывания функции f(x) = x³ - 3x²",
                                "answer": "Возрастает: (-∞, 0) ∪ (2, ∞), убывает: (0, 2)",
                                "difficulty": 1
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Текстовые задачи",
                "description": "Задачи на движение, работу, проценты, смеси и сплавы",
                "children": [
                    {
                        "title": "Задание 10",
                        "description": "Простые текстовые задачи",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 10.1",
                                "content": "Поезд проехал 120 км за 2 часа. Найдите скорость поезда",
                                "answer": "60 км/ч",
                                "difficulty": 1
                            }
                        ]
                    },
                    {
                        "title": "Задание 16",
                        "description": ":Экономические задачи: на вклады, кредиты, оптимизацию",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 16.1",
                                "content": "Вкладчик положил 10000 рублей под 10% годовых. Сколько будет на счете через 2 года?",
                                "answer": "12100 рублей",
                                "difficulty": 2
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Задача с параметром",
                "description": "Решение уравнений и неравенств с параметром",
                "children": [
                    {
                        "title": "Задание 18: Задача с параметром",
                        "description": "Аналитическое и графическое решение задач с параметром",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 18.1",
                                "content": "При каких a уравнение x² - 4x + a = 0 имеет два различных корня?",
                                "answer": "a < 4",
                                "difficulty": 2
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Числа и их свойства",
                "description": "Свойства чисел, делимость, четность, остатки",
                "children": [
                    {
                        "title": "Задание 19",
                        "description": "Задачи на делимость, простые числа, цифровую запись чисел",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 19.1",
                                "content": "Найдите наименьшее натуральное число, которое делится на 2, 3 и 5",
                                "answer": "30",
                                "difficulty": 1
                            }
                        ]
                    }
                ]
            }
        ]
    },
    {
        "title": "Теория вероятностей и статистика",
        "description": "Вероятность, комбинаторика, статистика",
        "children": [
            {
                "title": "Задание 4: Классическая вероятность",
                "description": "Задачи на классическую вероятность",
                "children": [],
                "tasks": [
                    {
                        "title": "Задание 4.1",
                        "content": "Бросают игральный кубик. Какова вероятность выпадения четного числа?",
                        "answer": "3/6 = 0.5",
                        "difficulty": 1
                    }
                ]
            },
            {
                "title": "Задание 5: Сложные вероятности",
                "description": "Условная вероятность, теоремы сложения и умножения",
                "children": [],
                "tasks": [
                    {
                        "title": "Задание 5.1",
                        "content": "Вероятность попадания в цель 0.8. Найдите вероятность попадания при двух выстрелах",
                        "answer": "0.96",
                        "difficulty": 2
                    },
                    {
                        "title": "Задание 5.2",
                        "content": "В ящике 5 белых и 3 черных шара. Вынимают два шара. Найдите вероятность, что оба белые",
                        "answer": "(5/8) × (4/7) = 20/56 = 5/14",
                        "difficulty": 2
                    }
                ]
            }
        ]
    },
    {
        "title": "Геометрия",
        "description": "Планиметрия и стереометрия",
        "children": [
            {
                "title": "Планиметрия",
                "description": "Геометрия на плоскости",
                "children": [
                    {
                        "title": "Задание 1",
                        "description": "Геометрические фигуры на плоскости и их свойства",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 1.1",
                                "content": "В треугольнике ABC угол A = 30°, угол B = 70°. Найдите угол C",
                                "answer": "80°",
                                "difficulty": 1
                            },
                            {
                                "title": "Задание 1.2",
                                "content": "Найдите площадь треугольника со сторонами 3, 4, 5",
                                "answer": "6",
                                "difficulty": 2
                            }
                        ]
                    },
                    {
                        "title": "Задание 17: Планиметрическая задача",
                        "description": "Сложные планиметрические задачи",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 17.1",
                                "content": "",
                                "answer": "",
                                "difficulty": 3
                            }
                        ]
                    }
                ]
            },
            {
                "title": "Стереометрия",
                "description": "Геометрия в пространстве",
                "children": [
                    {
                        "title": "Задание 3: Простые стереометрические задачи",
                        "description": "Геометрические фигуры в пространстве и их свойства",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 3.1",
                                "content": "Найдите объем куба с ребром 5 см",
                                "answer": "125 см³",
                                "difficulty": 1
                            }
                        ]
                    },
                    {
                        "title": "Задание 14: Стереометрическая задача",
                        "description": "Сложные стереометрические задачи",
                        "children": [],
                        "tasks": [
                            {
                                "title": "Задание 14.1",
                                "content": "",
                                "answer": "",
                                "difficulty": 3
                            }
                        ]
                    }
                ]
            }
        ]
    }
]


class Command(BaseCommand):
    """
    Management-команда для заполнения базы данных темами ЕГЭ
    """
    help = 'Заполняет базу данных темами ЕГЭ по математике (профильный уровень)'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Заполняю базу данных'))
        subject, created = Subject.objects.get_or_create(name="Математика (профиль)", defaults={"description": "Подготовка к ЕГЭ по математике профильного уровня"})
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создан предмет: {subject.name}'))

        stats = {'nodes': 0, 'lessons': 0, 'tasks': 0}
        def create_nodes(parent, children_data, level=0):
            indent = "  " * level
            for order, node_data in enumerate(children_data):
                node, created = RoadmapNode.objects.get_or_create(subject=subject, parent=parent, title=node_data["title"], defaults={
                        "description": node_data.get("description", ""),
                        "order": order,
                        "status": "unlocked" if parent is None else "locked"
                    }
                )

                if created:
                    stats['nodes'] += 1
                    self.stdout.write(self.style.SUCCESS(f'{indent} {node.title}'))
                    if node_data.get("tasks") is not None:
                        lesson, lesson_created = Lesson.objects.get_or_create(node=node,
                            defaults={
                                "title": f"Урок: {node.title}",
                                "content": "",
                                "order": 0
                            }
                        )
                        if lesson_created:
                            stats['lessons'] += 1
                            self.stdout.write(self.style.SUCCESS(f'{indent} Урок: {lesson.title}'))
                        for task_data in node_data.get("tasks", []):
                            task, task_created = Task.objects.get_or_create(
                                lesson=lesson,
                                title=task_data["title"],
                                defaults={
                                    "content": task_data["content"],
                                    "answer": task_data["answer"],
                                    "difficulty": task_data.get("difficulty", 1),
                                    "order": task_data.get("order", 0)
                                }
                            )
                            if task_created:
                                stats['tasks'] += 1
                                self.stdout.write(self.style.SUCCESS(f'{indent}  {task.title}'))
                if node_data.get("children"):
                    create_nodes(node, node_data["children"], level + 1)

        create_nodes(None, roadmap_data)

        self.stdout.write(self.style.SUCCESS(
            f'Создано:\n'
            f'  Предметов: {Subject.objects.count()}\n'
            f'  Тем: {stats["nodes"]}\n'
            f'  Уроков: {stats["lessons"]}\n'
            f'  Заданий: {stats["tasks"]}\n'
        ))