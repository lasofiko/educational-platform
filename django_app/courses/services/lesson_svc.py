from django.db.models import Prefetch
from courses.models import Lesson, Problem, RoadmapNode
from progress.models import UserProgress
from courses.exceptions import LessonNotFound, NodeLocked


class LessonService:
    """сервис для работы с уроками и задачами"""
    @staticmethod
    def get_lesson_with_problems(lesson_id, user):
        """получить урок со всеми задачами, проверив доступность ноды"""
        try:
            lesson = Lesson.objects.select_related('node').prefetch_related(Prefetch('problems', queryset=Problem.objects.order_by('order'))).get(id=lesson_id)
        except Lesson.DoesNotExist:
            raise LessonNotFound(lesson_id)
        try:
            user_progress = UserProgress.objects.get(user=user, node=lesson.node)
            if user_progress.status == 'locked':
                raise NodeLocked(lesson.node.id,f"Тема '{lesson.node.title}' заблокирована. Сначала выполните предыдущие задания.")
        except UserProgress.DoesNotExist:
            is_first_node = RoadmapNode.objects.filter(subject=lesson.node.subject,parent=None,order=0).first() == lesson.node
            if not is_first_node:
                raise NodeLocked(lesson.node.id,f"Тема '{lesson.node.title}' заблокирована. Сначала выполните предыдущие задания.")
        result = {
            'id': lesson.id,
            'title': lesson.title,
            'content': lesson.content,
            'order': lesson.order,
            'created_at': lesson.created_at,
            'node': {
                'id': lesson.node.id,
                'title': lesson.node.title,
                'node_type': lesson.node.node_type,
            },
            'problems': []
        }
        for problem in lesson.problems.all():
            result['problems'].append({
                'id': problem.id,
                'title': problem.title,
                'description': problem.description,
                'difficulty': problem.difficulty,
                'points': problem.points,
                'order': problem.order})
        return result
    @staticmethod
    def get_lessons_for_node(node_id):
        """получаем список всех уроков для указанной ноды"""
        lessons = Lesson.objects.filter(node_id=node_id).order_by('order')
        return [
            {
                'id': lesson.id,
                'title': lesson.title,
                'order': lesson.order,
                'created_at': lesson.created_at,
            }
            for lesson in lessons
        ]
    @staticmethod
    def get_problem_with_answer(problem_id, user):
        """получаем задачу с ответом и решением (для проверки)"""
        try:
            problem = Problem.objects.select_related('lesson__node').get(id=problem_id)
        except Problem.DoesNotExist:
            raise LessonNotFound(f"Задача с ID {problem_id} не найдена")
        try:
            user_progress = UserProgress.objects.get(user=user, node=problem.lesson.node)
            if user_progress.status == 'locked':
                raise NodeLocked(problem.lesson.node.id)
        except UserProgress.DoesNotExist:
            is_first_node = RoadmapNode.objects.filter(subject=problem.lesson.node.subject,parent=None,order=0).first() == problem.lesson.node
            if not is_first_node:
                raise NodeLocked(problem.lesson.node.id)
        return {
            'id': problem.id,
            'title': problem.title,
            'description': problem.description,
            'answer': problem.answer,
            'solution': problem.solution,
            'points': problem.points,
            'difficulty': problem.difficulty,
        }

def get_lesson_with_problems(lesson_id, user):
    return LessonService.get_lesson_with_problems(lesson_id, user)
def get_lessons_for_node(node_id):
    return LessonService.get_lessons_for_node(node_id)
def get_problem_with_answer(problem_id, user):
    return LessonService.get_problem_with_answer(problem_id, user)