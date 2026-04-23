import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from django.db import IntegrityError

class TestDomainException:
    def test_exception_has_code_and_detail(self):
        from courses.exceptions import DomainException
        exc = DomainException("test_code", "test_detail")
        assert exc.code == "test_code"
        assert exc.detail == "test_detail"

class TestNodeLocked:
    def test_exception_has_correct_code(self):
        from courses.exceptions import NodeLocked
        exc = NodeLocked("Заблокировано")
        assert exc.code == "node_locked"

    def test_handler_returns_403(self):
        from courses.exceptions import custom_exception_handler, NodeLocked
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = Request(factory.get('/'))
        response = custom_exception_handler(NodeLocked("test"), {'request': request})

        assert response.status_code == 403
        assert response.data == {"error": {"code": "node_locked", "detail": "test"}}

class TestAlreadyEnrolled:
    def test_exception_has_correct_code(self):
        from courses.exceptions import AlreadyEnrolled
        exc = AlreadyEnrolled("Уже записан")
        assert exc.code == "already_enrolled"

    def test_handler_returns_400(self):
        from courses.exceptions import custom_exception_handler, AlreadyEnrolled
        from rest_framework.request import Request
        from rest_framework.test import APIRequestFactory

        factory = APIRequestFactory()
        request = Request(factory.get('/'))
        response = custom_exception_handler(AlreadyEnrolled("test"), {'request': request})

        assert response.status_code == 400
        assert response.data == {"error": {"code": "already_enrolled", "detail": "test"}}

class TestStandardDRFErrors:
    @pytest.mark.django_db
    def test_404_not_found(self):
        client = APIClient()
        response = client.get('/api/v1/courses/subjects/99999/')
        assert response.status_code == 404

    @pytest.mark.django_db
    def test_400_bad_request(self):
        client = APIClient()
        response = client.post('/api/v1/accounts/register/', {
            'username': 'test',
            'password': '123',
            'password2': '456'
        })
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_401_unauthorized(self):
        client = APIClient()
        response = client.get('/api/v1/accounts/me/')
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_enrollment_unique_constraint(self):
        from progress.models import Enrollment
        from courses.models import Subject

        user = User.objects.create_user(username='test', password='pass')
        subject = Subject.objects.create(name="Math")

        Enrollment.objects.create(user=user, subject=subject)

        with pytest.raises(IntegrityError):
            Enrollment.objects.create(user=user, subject=subject)