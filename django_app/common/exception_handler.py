from rest_framework.views import exception_handler
from rest_framework.response import Response
from django_app.common.exceptions import DomainExceptions

def custom_exception_handler(exc, context):
    if isinstance(exc, DomainExceptions):
        data={
            "error" : {
                "code" : exc.code,
                "detail" : exc.detail,
            }
        }
        return Response(data, status=exc.status_code)
    
    response = exception_handler(exc, context)
    return response

