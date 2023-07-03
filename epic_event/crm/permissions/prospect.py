from django.contrib.auth.models import Permission

from authentication.exceptions import AccessDenied
from ..models import Prospect
from .basepermission import CustomBasePermission

class ProspectPermission(CustomBasePermission):
    model = Prospect

    def has_object_permission(self, request, view, obj):
        super().has_object_permission(request, view, obj)
        if view.action == 'to_client':
            permission_natural_key = Permission.objects.get(codename=f'change_{self.model.__name__.lower()}').natural_key()
            if not request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
                raise AccessDenied(f'You don\'t have change permission for {self.model.__name__} !', request=request)
        return True