from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Subject, RoadmapNode, Lesson, Problem, Quiz
from .serializers import (
    SubjectSerializer,
    RoadmapNodeSerializer,
    RoadmapNodeDetailSerializer,
    LessonSerializer,
    ProblemSerializer,
    ProblemDetailSerializer,
    QuizSerializer
)
from .filters import ProblemFilter, LessonFilter
from .services import roadmap_svc, lesson_svc, subject_svc

class SubjectViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = SubjectSerializer

    def get_queryset(self):
        return subject_svc.get_all_subjects()

class RoadmapViewSet(viewsets.GenericViewSet):

    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RoadmapNodeDetailSerializer
        return RoadmapNodeSerializer

    # дерево тем
    def list(self, request):
        subject_id = request.query_params.get('subject_id')
        nodes = roadmap_svc.get_tree(subject_id=subject_id)
        return Response(nodes)

    # детальная информация о теме с уроками
    def retrieve(self, request, pk=None):
        node = roadmap_svc.get_node_with_status(pk, user=request.user)
        if node is None:
            return Response({'error': 'Тема не найдена'}, status=404)
        serializer = self.get_serializer(node, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='progress')
    def progress(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'error': 'Требуется авторизация'}, status=401)

        node = roadmap_svc.get_node_with_status(pk, request.user)
        return Response({
            'node_id': pk,
            'status': node['user_status'],
            'score': node['user_score'],
            'completed_at': node['user_completed_at'],
        })

class LessonViewSet(viewsets.GenericViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = LessonSerializer

    def retrieve(self, request, pk=None):
        lesson = lesson_svc.get_lesson_with_problems(pk, request.user)
        if lesson is None:
            return Response({'error': 'Урок не найден'}, status=404)
        serializer = self.get_serializer(lesson)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-node/(?P<node_id>[^/.]+)')
    def by_node(self, request, node_id=None):

        lessons = lesson_svc.get_lessons_for_node(node_id)
        return Response(lessons)

class ProblemViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [permissions.AllowAny]
    filterset_class = ProblemFilter

    def get_queryset(self):
        return Problem.objects.select_related('lesson__node__subject').all().order_by('order')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProblemDetailSerializer
        return ProblemSerializer

class QuizViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = [permissions.AllowAny]
    serializer_class = QuizSerializer

    def get_queryset(self):
        return Quiz.objects.prefetch_related('questions').all()