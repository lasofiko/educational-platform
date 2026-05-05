from rest_framework.views import exception_handler
from rest_framework.response import Response
from common.exceptions import DomainException


def custom_exception_handler(exc, context):
    if isinstance(exc, DomainException):
        return Response({
            'error': {
                'code': exc.code,
                'detail': exc.message,
            }
        }, status=exc.status_code)
    return exception_handler(exc, context)
