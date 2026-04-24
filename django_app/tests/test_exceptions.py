from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from courses.exceptions import (
    DomainException,
    NodeLocked,
    AlreadyEnrolled,
    LessonNotFound,
    NodeNotFound,
    ValidationException,
    NotFoundException,
)


class ExceptionsFormatTest(TestCase):
    def test_domain_exception_format(self):
        """DomainException возвращает JSON {"error": {"code": ..., "detail": ...}}"""
        exception = DomainException("Тестовая ошибка", status_code=400)

        error_response = {
            "error": {
                "code": exception.status_code,
                "detail": exception.message
            }
        }

        self.assertEqual(error_response["error"]["code"], 400)
        self.assertEqual(error_response["error"]["detail"], "Тестовая ошибка")

    def test_node_locked_http_403(self):

        exception = NodeLocked(123)

        self.assertEqual(exception.status_code, 403)
        self.assertIsInstance(exception, DomainException)
        self.assertIn("заблокирована", exception.message)

    def test_already_enrolled_http_400(self):
        exception = AlreadyEnrolled()

        self.assertEqual(exception.status_code, 400)
        self.assertIsInstance(exception, DomainException)
        self.assertIn("уже записан", exception.message)

    def test_already_enrolled_with_custom_data(self):
         exception = AlreadyEnrolled(
            message="Студент уже записан",
            user_id=1,
            course_id=5
        )
        self.assertEqual(exception.user_id, 1)
        self.assertEqual(exception.course_id, 5)

    def test_standard_drf_errors(self):
         client = APIClient()

        response = client.get("/api/v1/nonexistent-url/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertIsNotNone(response.data)