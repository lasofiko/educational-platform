import django_filters
from .models import Problem, Lesson

# для задач
class ProblemFilter(django_filters.FilterSet):
    # по сложности
    difficulty = django_filters.ChoiceFilter(
        choices=Problem.DIFFICULTY_CHOICES,
        field_name='difficulty',
        lookup_expr='exact'
    )
    # по уроку
    lesson = django_filters.NumberFilter(
        field_name='lesson__id',
        lookup_expr='exact'
    )
    # по предмету
    lesson__node__subject = django_filters.NumberFilter(
        field_name='lesson__node__subject__id',
        lookup_expr='exact',
        label='Subject ID'
    )
    class Meta:
        model = Problem
        fields = ['difficulty', 'lesson', 'lesson__node__subject']

# для уроков
class LessonFilter(django_filters.FilterSet):
    # по теме
    node = django_filters.NumberFilter(
        field_name='node__id',
        lookup_expr='exact'
    )
    # по предмету
    node__subject = django_filters.NumberFilter(
        field_name='node__subject__id',
        lookup_expr='exact',
        label='Subject ID'
    )
    class Meta:
        model = Lesson
        fields = ['node', 'node__subject']