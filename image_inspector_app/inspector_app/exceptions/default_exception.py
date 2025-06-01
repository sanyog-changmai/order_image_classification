from rest_framework.exceptions import APIException
from rest_framework import status


class DefaultException(Exception):
    def __init__(self, message):
        message = {
            "error": {
                "success": False,
                "message": message,
                "developer_message": message,
                "status_code": status.HTTP_503_SERVICE_UNAVAILABLE
            }
        }
        self.message = message
