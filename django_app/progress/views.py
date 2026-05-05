from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProgress
from .serializers import (
    EnrollmentSerializer,
    UserProgressSerializer,
    AnswerSubmitSerializer,
    QuizSubmitSerializer,
)
from .services import enrollment_svc
from .services.scoring_svc import ScoringService
from .exceptions import NotEnrolled


class EnrollmentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrollmentSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        try:
            return enrollment_svc.get_user_enrollments(self.request.user)
        except NotEnrolled:
            return self.serializer_class.Meta.model.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        enrollment = enrollment_svc.enroll(request.user, serializer.validated_data['subject'].id)
        return Response(self.get_serializer(enrollment).data, status=status.HTTP_201_CREATED)


class UserProgressViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProgressSerializer

    def get_queryset(self):
        return UserProgress.objects.filter(user=self.request.user).select_related('node').order_by('-updated_at')

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response(
                {'error': {'code': 'validation_error', 'detail': 'subject_id is required'}},
                status=status.HTTP_400_BAD_REQUEST,
            )
        nodes_completed, average_score = ScoringService.get_user_progress(request.user, subject_id)
        return Response({
            'subject_id': int(subject_id),
            'nodes_completed': nodes_completed,
            'average_score': average_score,
        })


class SubmitAnswerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = AnswerSubmitSerializer(data={'problem_id': pk, **request.data})
        serializer.is_valid(raise_exception=True)
        result = ScoringService.submit_answer(request.user, pk, serializer.validated_data['answer'])
        return Response(result)


class SubmitQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        serializer = QuizSubmitSerializer(data={'quiz_id': pk, **request.data})
        serializer.is_valid(raise_exception=True)
        result = ScoringService.calculate_quiz_score(request.user, pk, serializer.validated_data['answers'])
        return Response(result)
