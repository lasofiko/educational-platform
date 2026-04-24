from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'roadmap', views.RoadmapViewSet, basename='roadmap')
router.register(r'lessons', views.LessonViewSet, basename='lesson')
router.register(r'problems', views.ProblemViewSet, basename='problem')
router.register(r'quizzes', views.QuizViewSet, basename='quiz')

urlpatterns = [
    path('', include(router.urls)),
]

app_name = 'courses'