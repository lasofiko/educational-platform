from rest_framework import serializers
from .models import Enrollment, UserProgress


class EnrollmentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Enrollment
        fields = ('id', 'user', 'subject', 'enrolled_at')


class UserProgressSerializer(serializers.ModelSerializer):
    node_title = serializers.SerializerMethodField()

    class Meta:
        model = UserProgress
        fields = ('id', 'user', 'node', 'node_title', 'status', 'score',
                  'completed_at', 'created_at', 'updated_at')
        read_only_fields = fields

    def get_node_title(self, obj):
        return obj.node.title


class AnswerSubmitSerializer(serializers.Serializer):
    problem_id = serializers.IntegerField()
    answer = serializers.CharField(max_length=500)


class QuizSubmitSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = serializers.DictField(child=serializers.CharField())
