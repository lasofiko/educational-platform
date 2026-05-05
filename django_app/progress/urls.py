from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r'enrollments', views.EnrollmentViewSet, basename='enrollment')
router.register(r'my', views.UserProgressViewSet, basename='userprogress')

urlpatterns = [
    path('', include(router.urls)),
    path('problems/<int:pk>/submit/', views.SubmitAnswerView.as_view(), name='submit-answer'),
    path('quizzes/<int:pk>/submit/', views.SubmitQuizView.as_view(), name='submit-quiz'),
]

app_name = 'progress'
