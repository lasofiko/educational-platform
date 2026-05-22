from django.core.management.base import BaseCommand
from django.db import transaction
from courses.models import Subject, RoadmapNode, Lesson, Problem

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
                        "problems": [
                            {
                                "title": "Задание 9.1",
                                "description": "",
                                "answer": "",
                                "difficulty": "easy"
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
                        "problems": [
                            {
                                "title": "Задание 2.1",
                                "description": "Найдите скалярное произведение векторов a(1, 2) и b(3, 4)",
                                "answer": "1×3 + 2×4 = 3 + 8 = 11",
                                "difficulty": "easy"
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
                        "problems": [
                            {
                                "title": "Задание 6.1",
                                "description": "",
                                "answer": "",
                                "difficulty": "easy"
                            }
                        ]
                    },
                    {
                        "title": "Задание 7",
                        "description": "Вычисления и преобразования",
                        "children": [],
                        "problems": [
                            {
                                "title": "Задание 7.1",
                                "description": "",
                                "answer": "",
                                "difficulty": "easy"
                            }
                        ]
                    },
                    {
                        "title": "Задание 13",
                        "description": "Тригонометрические уравнения",
                        "children": [],
                        "problems": [
                            {
                                "title": "Задание 13.1",
                                "description": "Решите уравнение: sin²x + sin x = 0",
                                "answer": "x = πn, x = -π/2 + 2πn, x = 3π/2 + 2πn, n ∈ Z",
                                "difficulty": "medium"
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
                        "problems": [
                            {
                                "title": "Задание 13.1",
                                "description": "Решите неравенство: log₂(x + 3) < 2",
                                "answer": "-3 < x < 1",
                                "difficulty": "medium"
                            }
                        ]
                    },
                    {
                        "title": "Задание 15",
                        "description": "Решение рациональных, иррациональных и показательных неравенств",
                        "children": [],
                        "problems": [
                            {
                                "title": "Задание 15.1",
                                "description": "Решите неравенство: x² - 4x + 3 > 0",
                                "answer": "x < 1 или x > 3",
                                "difficulty": "easy"
                            },
                            {
                                "title": "Задание 15.2",
                                "description": "Решите неравенство: 2ˣ > 8",
                                "answer": "x > 3",
                                "difficulty": "easy"
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
                        "problems": [
                            {
                                "title": "Задание 11.2",
                                "description": "По графику функции определите промежутки возрастания",
                                "answer": "Зависит от графика",
                                "difficulty": "easy"
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
                        "problems": [
                            {
                                "title": "Задание 8.1",
                                "description": "Найдите точки экстремума функции f(x) = x³ - 3x²",
                                "answer": "x = 0 (max), x = 2 (min)",
                                "difficulty": "easy"
                            }
                        ]
                    },
                    {
                        "title": "Задание 12: Исследование функций",
                        "description": "Полное исследование функций с помощью производной",
                        "children": [],
                        "problems": [
                            {
                                "title": "Задание 12.1",
                                "description": "Найдите промежутки возрастания и убывания функции f(x) = x³ - 3x²",
                                "answer": "Возрастает: (-∞, 0) ∪ (2, ∞), убывает: (0, 2)",
                                "difficulty": "easy"
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
                        "problems": [
                            {
                                "title": "Задание 10.1",
                                "description": "Поезд проехал 120 км за 2 часа. Найдите скорость поезда",
                                "answer": "60 км/ч",
                                "difficulty": "easy"
                            }
                        ]
                    },
                    {
                        "title": "Задание 16",
                        "description": ":Экономические задачи: на вклады, кредиты, оптимизацию",
                        "children": [],
                        "problems": [
                            {
                                "title": "Задание 16.1",
                                "description": "Вкладчик положил 10000 рублей под 10% годовых. Сколько будет на счете через 2 года?",
                                "answer": "12100 рублей",
                                "difficulty": "medium"
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
                        "problems": [
                            {
                                "title": "Задание 18.1",
                                "description": "При каких a уравнение x² - 4x + a = 0 имеет два различных корня?",
                                "answer": "a < 4",
                                "difficulty": "medium"
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
                        "problems": [
                            {
                                "title": "Задание 19.1",
                                "description": "Найдите наименьшее натуральное число, которое делится на 2, 3 и 5",
                                "answer": "30",
                                "difficulty": "easy"
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
                "problems": [
                    {
                        "title": "Задание 4.1",
                        "description": "Бросают игральный кубик. Какова вероятность выпадения четного числа?",
                        "answer": "3/6 = 0.5",
                        "difficulty": "easy"
                    }
                ]
            },
            {
                "title": "Задание 5: Сложные вероятности",
                "description": "Условная вероятность, теоремы сложения и умножения",
                "children": [],
                "problems": [
                    {
                        "title": "Задание 5.1",
                        "description": "Вероятность попадания в цель 0.8. Найдите вероятность попадания при двух выстрелах",
                        "answer": "0.96",
                        "difficulty": "medium"
                    },
                    {
                        "title": "Задание 5.2",
                        "description": "В ящике 5 белых и 3 черных шара. Вынимают два шара. Найдите вероятность, что оба белые",
                        "answer": "(5/8) × (4/7) = 20/56 = 5/14",
                        "difficulty": "medium"
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
                        "problems": [
                            {
                                "title": "Задание 1.1",
                                "description": "В треугольнике ABC угол A = 30°, угол B = 70°. Найдите угол C",
                                "answer": "80°",
                                "difficulty": "easy"
                            },
                            {
                                "title": "Задание 1.2",
                                "description": "Найдите площадь треугольника со сторонами 3, 4, 5",
                                "answer": "6",
                                "difficulty": "medium"
                            }
                        ]
                    },
                    {
                        "title": "Задание 17: Планиметрическая задача",
                        "description": "Сложные планиметрические задачи",
                        "children": [],
                        "problems": [
                            {
                                "title": "Задание 17.1",
                                "description": "",
                                "answer": "",
                                "difficulty": "hard"
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
                        "problems": [
                            {
                                "title": "Задание 3.1",
                                "description": "Найдите объем куба с ребром 5 см",
                                "answer": "125 см³",
                                "difficulty": "easy"
                            }
                        ]
                    },
                    {
                        "title": "Задание 14: Стереометрическая задача",
                        "description": "Сложные стереометрические задачи",
                        "children": [],
                        "problems": [
                            {
                                "title": "Задание 14.1",
                                "description": "",
                                "answer": "",
                                "difficulty": "hard"
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
        subject, created = Subject.objects.get_or_create(
            name="Математика (профиль)",
            defaults={"description": "Подготовка к ЕГЭ по математике профильного уровня", "icon": "math"},
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Создан предмет: {subject.name}'))

        extra_subjects = [
            ("Русский язык", "Подготовка к ЕГЭ по русскому языку", "russian"),
            ("Информатика", "Подготовка к ЕГЭ по информатике", "informatics"),
        ]
        for name, description, icon in extra_subjects:
            obj, was_created = Subject.objects.get_or_create(
                name=name,
                defaults={"description": description, "icon": icon},
            )
            if was_created:
                self.stdout.write(self.style.SUCCESS(f'Создан предмет: {obj.name}'))

        stats = {'nodes': 0, 'lessons': 0, 'problems': 0}
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
                    if node_data.get("problems") is not None:
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
                        for task_data in node_data.get("problems", []):
                            task, task_created = Problem.objects.get_or_create(
                                lesson=lesson,
                                title=task_data["title"],
                                defaults={
                                    "description": task_data["description"],
                                    "answer": task_data["answer"],
                                    "difficulty": task_data.get("difficulty", "easy"),
                                    "order": task_data.get("order", 0)
                                }
                            )
                            if task_created:
                                stats['problems'] += 1
                                self.stdout.write(self.style.SUCCESS(f'{indent}  {task.title}'))
                if node_data.get("children"):
                    create_nodes(node, node_data["children"], level + 1)

        create_nodes(None, roadmap_data)

        self.stdout.write(self.style.SUCCESS(
            f'Создано:\n'
            f'  Предметов: {Subject.objects.count()}\n'
            f'  Тем: {stats["nodes"]}\n'
            f'  Уроков: {stats["lessons"]}\n'
            f'  Заданий: {stats["problems"]}\n'
        ))