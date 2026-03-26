from django.contrib import admin
from .models import Subject, RoadmapNode, Lesson, Task

admin.site.register(Subject)
admin.site.register(RoadmapNode)
admin.site.register(Lesson)
admin.site.register(Task)
