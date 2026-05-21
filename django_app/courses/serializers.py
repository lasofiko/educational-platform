from rest_framework import serializers
from .models import Subject, RoadmapNode, Lesson, Problem, Quiz, QuizQuestion
from .services.ugc_client import get_ugc_summary

# все поля модели
class SubjectSerializer(serializers.ModelSerializer):
    ugc_summary = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        view = self.context.get('view')
        if getattr(view, 'action', None) != 'retrieve':
            self.fields.pop('ugc_summary', None)

    def get_ugc_summary(self, obj):
        return get_ugc_summary('subject', obj.id)

# сериализует задачу, но при запросе списка задач скрывает ответ и решение
class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        view = self.context.get('view')
        if getattr(view, 'action', None) == 'list':
            self.fields.pop('answer', None)
            self.fields.pop('solution', None)


class ProblemDetailSerializer(ProblemSerializer):
    class Meta(ProblemSerializer.Meta):
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

# сериализует урок и подтягивает задачи
class LessonSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'

#скрывает правильный ответ, чтобы ученик не мог подсмотреть
class QuizQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizQuestion
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # не отдаём правильные ответы ни в list, ни в retrieve квиза (courses API)
        data.pop('answer', None)
        return data

#сериализует тесты и подтягивает вопросы
class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = '__all__'

#сериализует дерево с темами
class RoadmapNodeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = RoadmapNode
        fields = (
            'id', 'subject', 'parent', 'title', 'task_number',
            'description', 'node_type', 'order', 'status', 'children'
        )
        read_only_fields = ('status',)

    def get_children(self, obj):
        children = obj.children.all().order_by('order')
        if children:
            return RoadmapNodeSerializer(children, many=True, context=self.context).data
        return []

    def get_status(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return 'locked'

        user_progress = getattr(request.user, 'progress', None)
        if user_progress is not None:
            try:
                progress = user_progress.filter(node=obj).first()
                if progress:
                    return progress.status
            except Exception:
                pass

        if obj.parent is None:
            return 'unlocked'
        return 'locked'

#добавляет поле со списком уроков по теме
class RoadmapNodeDetailSerializer(RoadmapNodeSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta(RoadmapNodeSerializer.Meta):
        fields = RoadmapNodeSerializer.Meta.fields + ('lessons',)