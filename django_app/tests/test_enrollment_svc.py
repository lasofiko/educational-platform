import pytest
from progress.services.enrollment_svc import enroll
from progress.exceptions import AlreadyEnrolled
from courses.models import Subject
from django.contrib.auth import get_user_model

User = get_user_model()
@pytest.fixture
def data(db):
    subject=Subject.objects.create()
    user=User.objects.create()
    return user,subject

@pytest.mark.django_db
def test_enroll(data):
    user, subject=data
    result=enroll(user, subject.id)
    assert result is not None

@pytest.mark.django_db
def test_already_enrolled(data):
    user, subject=data
    enroll(user, subject.id)
    with pytest.raises(AlreadyEnrolled):
        enroll(user, subject.id)

@pytest.mark.django_db
def test_fake_subject(data):
    user, _ =data
    with pytest.raises(Exception):
        enroll(user, 9999)