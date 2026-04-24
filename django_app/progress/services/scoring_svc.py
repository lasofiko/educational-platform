from django.db.models import Avg
from django.db.models import F
from django.utils import timezone
from django_app.courses.models import Problem
from django_app.progress.models import UserProgress


def get_user_progress(user,subject_id):
    first_count = UserProgress.objects.filter(user= user,node__subject_id = subject_id,status='complete')

    nodes_count = first_count.count()

    progress_stats = UserProgress.objects.filter(user = user,node__subject_id = subject_id).aggregate(average = Avg('score'))

    avg = progress_stats['average'] or 0

    return nodes_count, round(avg,2)

def submit_answer(user,problem_id,answer):
    problem = Problem.objects.get(id=problem_id)
    if answer.strip().lower() == problem.answer.strip().lower():
        progress, _ = UserProgress.objects.get_or_create(user = user,node= problem.lesson.node, defaults = {'score' : 0})

        progress.status = 'completed'
        progress.score = F('score')+problem.points
        progress.completed_at = timezone.now()
        progress.save()

        return {'correct' : True, 'points' : problem.points}

    return {'correct' : False, 'points' : 0}


    