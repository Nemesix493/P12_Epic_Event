from django.contrib.auth.models import Permission

from ..models import Event
from authentication.models import ManageMember
from authentication.exceptions import AccessDenied
from .basepermission import CustomBasePermission

class EventPermission(CustomBasePermission):
    model = Event

    def has_object_permission(self, request, view, obj: Event):
        if request.user.is_authenticated:
            if (view.action == 'update' or view.action == 'partial_update') and request.user.children == obj.support_contact:
                return True
            elif view.action == 'set_support':
                permission_natural_key = Permission.objects.get(codename=f'set_support_event').natural_key()
                if request.user.has_perm(f'{permission_natural_key[1]}.{permission_natural_key[0]}'):
                    return True
                else:
                    raise AccessDenied('You don\'t have set support permission !')
        return super().has_object_permission(request, view, obj)