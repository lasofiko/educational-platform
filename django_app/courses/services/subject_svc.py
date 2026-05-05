from courses.models import Subject


def get_all_subjects():
    return Subject.objects.all().order_by('name')


def get_subject(subject_id):
    return Subject.objects.get(id=subject_id)
