from django.contrib import admin

from .models import Subject, RoadmapNode, Lesson, Problem, Quiz, QuizQuestion

admin.site.register(Subject)
admin.site.register(RoadmapNode)
admin.site.register(Lesson)
admin.site.register(Problem)
admin.site.register(Quiz)
admin.site.register(QuizQuestion)
