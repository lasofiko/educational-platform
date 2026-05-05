from django_app.progress.models import Enrollment
from django_app.courses.models import Subject
from django_app.progress.exceptions import AlreadyEnrolled,NotEnrolled,SubjectNotFound

def enroll(user,subject_id):
    if not Subject.objects.filter(id=subject_id).exists():
        raise SubjectNotFound
    if Enrollment.objects.filter(user=user,subject_id=subject_id).exists():
        raise AlreadyEnrolled
    return Enrollment.objects.create(user=user,subject_id=subject_id)



def get_user_enrollments(user):
    enrollments = Enrollment.objects.filter(user=user).select_related("subject")
    if not enrollments.exists():
        raise NotEnrolled
    return enrollments