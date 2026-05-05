from django.db.models import Avg, Model
from django.db.models import F
from django.utils import timezone
from django_app.courses.models import Problem, Quiz, QuizQuestion
from django_app.progress.exceptions import QuizFailed
from django_app.progress.models import UserProgress
from django_app.courses.services.roadmap_svc import RoadmapService, unlock_next_node


class ScoringService:
    @staticmethod
    def get_user_progress(user, subject_id):
        first_count = UserProgress.objects.filter(user=user, node__subject_id=subject_id, status='complete')

        nodes_count = first_count.count()

        progress_stats = UserProgress.objects.filter(user=user, node__subject_id=subject_id).aggregate(
            average=Avg('score'))

        avg = progress_stats['average'] or 0

        return nodes_count, round(avg, 2)

    @staticmethod
    def submit_answer(user, problem_id, answer):
        problem = Problem.objects.get(id=problem_id)
        if answer.strip().lower() == problem.answer.strip().lower():
            progress, _ = UserProgress.objects.get_or_create(user=user, node=problem.lesson.node, defaults={'score': 0})

            progress.status = 'completed'
            progress.score = F('score') + problem.points
            progress.completed_at = timezone.now()
            progress.save()

            return {'correct': True, 'points': problem.points}

        return {'correct': False, 'points': 0}

    @staticmethod
    def calculate_quiz_score(user, quiz_id, answers):
        quiz=Quiz.objects.get(id=quiz_id)
        questions = QuizQuestion.objects.filter(quiz=quiz)
        total_questions = questions.count()

        if total_questions == 0:
            return  {'percentage' : 0,'passed' : False, "message" : "No questions found"}

        correct_answers = {q.id :q.answer for q in questions}

        correct_count=0

        for q_id, answer in answers.items():
            q_id=int(q_id)
            correct_answer=correct_answers.get(q_id)
            if correct_answer and answer.strip().lower()==correct_answer.strip().lower():
                correct_count+=1

        percentage = (correct_count / total_questions) * 100

        if percentage >= quiz.passing_score:

             current_node_id=quiz.lesson.node.id

             un=unlock_next_node(user, current_node_id,percentage)

             return {"percentage" : round(percentage,2), "passed" : True,"message" : "Pass", "unlocked nodes" : un}

        raise QuizFailed(detail=f"Тест не пройден. Ваш результат:{percentage}. Необходимый результат : {quiz.passing_score}")

