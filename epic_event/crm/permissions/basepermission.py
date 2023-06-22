from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Permission

from authentication.exceptions import AccessDenied

class CustomBasePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            raise AccessDenied('You must be authenticated !', 'not_authenticated')
        if view.action == 'retrieve':
            permission_natural_key = Permission.objects.get(codename=f'view_{self.model.__name__.lower()}').natural_key()
            if not request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
                raise AccessDenied(f'You don\'t have view permission for {self.model.__name__} !')
        elif view.action == 'update' or view.action == 'partial_update':
            permission_natural_key = Permission.objects.get(codename=f'change_{self.model.__name__.lower()}').natural_key()
            if not request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
                raise AccessDenied(f'You don\'t have change permission for {self.model.__name__} !')
        elif view.action == 'destroy':
            permission_natural_key = Permission.objects.get(codename=f'delete_{self.model.__name__.lower()}').natural_key()
            if not request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
                raise AccessDenied(f'You don\'t have delete permission for {self.model.__name__} !')
        return True
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise AccessDenied('You must be authenticated !', 'not_authenticated')
        if view.action == 'list':
            permission_natural_key = Permission.objects.get(codename=f'view_{self.model.__name__.lower()}').natural_key()
            if not request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
                raise AccessDenied(f'You don\'t have view permission for {self.model.__name__} !')
        elif view.action == 'create':
            permission_natural_key = Permission.objects.get(codename=f'add_{self.model.__name__.lower()}').natural_key()
            if not request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
                raise AccessDenied(f'You don\'t have add permission for {self.model.__name__} ! {request.user.get_all_permissions()}')
        return True