from rest_framework import status
from rest_framework.exceptions import APIException


class AccessDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Access denied !'
    default_code = 'access_denied'


class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request !'
    default_code = 'bad_request'

class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found !'
    default_code = 'not_found'
