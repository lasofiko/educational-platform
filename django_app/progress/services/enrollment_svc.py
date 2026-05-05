from courses.models import Subject
from progress.models import Enrollment
from progress.exceptions import AlreadyEnrolled, NotEnrolled, SubjectNotFound


def enroll(user, subject_id):
    if not Subject.objects.filter(id=subject_id).exists():
        raise SubjectNotFound()
    if Enrollment.objects.filter(user=user, subject_id=subject_id).exists():
        raise AlreadyEnrolled(user_id=user.id, course_id=subject_id)
    return Enrollment.objects.create(user=user, subject_id=subject_id)


def get_user_enrollments(user):
    enrollments = Enrollment.objects.filter(user=user).select_related('subject')
    if not enrollments.exists():
        raise NotEnrolled()
    return enrollments
