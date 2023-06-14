from rest_framework.permissions import BasePermission
from rest_framework.exceptions import APIException
from rest_framework import status

from ..models import ManageMember
from ..exceptions import AccessDenied

class UserPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise AccessDenied('You must be authenticated !', 'not_authenticated')
        if not isinstance(request.user.children, ManageMember):
            raise AccessDenied('You must be a manage member !')
        return True
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AccessDenied('You must be authenticated !', 'not_authenticated')
        if not isinstance(request.user.children, ManageMember):
            raise AccessDenied('You must be a manage member !')
        return True