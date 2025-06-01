from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    message = {
        "success": False,
        "message": 'OOPs something went wrong !',
        "developer_message": str(exc),
        "status_code": status.HTTP_503_SERVICE_UNAVAILABLE
    }

    return Response(message, status.HTTP_503_SERVICE_UNAVAILABLE)
