from django.db.models import Avg, F
from django.utils import timezone

from courses.models import Problem, Quiz, QuizQuestion
from courses.services.roadmap_svc import unlock_next_node
from progress.models import UserProgress
from progress.exceptions import ProblemNotFound, QuizFailed, QuizNotFound
from progress.notifications_client import notify_node_unlocked

class ScoringService:
    @staticmethod
    def get_user_progress(user, subject_id):
        completed = UserProgress.objects.filter(
            user=user, node__subject_id=subject_id, status='complete'
        )
        nodes_count = completed.count()

        stats = UserProgress.objects.filter(
            user=user, node__subject_id=subject_id
        ).aggregate(average=Avg('score'))
        avg = stats['average'] or 0

        return nodes_count, round(avg, 2)

    @staticmethod
    def submit_answer(user, problem_id, answer):
        try:
            problem = Problem.objects.select_related('lesson__node').get(id=problem_id)
        except Problem.DoesNotExist:
            raise ProblemNotFound(problem_id=problem_id)

        if answer.strip().lower() == problem.answer.strip().lower():
            progress, _ = UserProgress.objects.get_or_create(
                user=user, node=problem.lesson.node, defaults={'score': 0}
            )
            progress.status = 'complete'
            progress.score = F('score') + problem.points
            progress.completed_at = timezone.now()
            progress.save()
            return {'correct': True, 'points': problem.points}

        return {'correct': False, 'points': 0}

    @staticmethod
    def calculate_quiz_score(user, quiz_id, answers):
        try:
            quiz = Quiz.objects.select_related('lesson__node').get(id=quiz_id)
        except Quiz.DoesNotExist:
            raise QuizNotFound(quiz_id=quiz_id)

        questions = QuizQuestion.objects.filter(quiz=quiz)
        total = questions.count()
        if total == 0:
            return {'percentage': 0, 'passed': False, 'message': 'No questions found'}

        correct_answers = {q.id: q.answer for q in questions}
        correct_count = 0
        for q_id, answer in answers.items():
            q_id = int(q_id)
            correct_answer = correct_answers.get(q_id)
            if correct_answer and answer.strip().lower() == correct_answer.strip().lower():
                correct_count += 1

        percentage = (correct_count / total) * 100

        if percentage >= quiz.passing_score:
            unlocked = unlock_next_node(user, quiz.lesson.node.id, percentage)

            if isinstance(unlocked, dict):
                notify_node_unlocked(user.id, unlocked["id"], unlocked["title"])
            elif isinstance(unlocked, list):
                for node in unlocked:
                    notify_node_unlocked(user.id, node["id"], node["title"])
            
            return {
                'percentage': round(percentage, 2),
                'passed': True,
                'message': 'Pass',
                'unlocked_nodes': unlocked,
            }

        raise QuizFailed(
            message=f'Тест не пройден. Ваш результат: {round(percentage, 2)}%. '
                    f'Необходимый результат: {quiz.passing_score}%'
        )
