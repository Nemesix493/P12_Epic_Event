import logging
import datetime

from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger('django')

class LoggedAPIException(APIException):
    def __init__(self, detail=None, code=None, request=None):
        super().__init__(detail, code)
        if request != None:
            logger.error(f'An exception occurred in API:{self}:{datetime.datetime.now()}:{request.build_absolute_uri()}:{request.method}:{request.META.get("REMOTE_ADDR")}')
        else:
            logger.exception(f'An exception occurred in API:{self}:{datetime.datetime.now()}')
        


class AccessDenied(LoggedAPIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'Access denied !'
    default_code = 'access_denied'


class BadRequest(LoggedAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad request !'
    default_code = 'bad_request'

class NotFound(LoggedAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found !'
    default_code = 'not_found'
