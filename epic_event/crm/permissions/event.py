from ..models import Event
from authentication.models import ManageMember
from authentication.exceptions import AccessDenied
from .basepermission import CustomBasePermission

class EventPermission(CustomBasePermission):
    model = Event

    def has_object_permission(self, request, view, obj: Event):
        if (view.action == 'update' or view.action == 'partial_update') and request.user.children == obj.support_contact:
            return True
        elif view.action == 'set_support':
            if isinstance(request.user.children, ManageMember):
                return True
            else:
                raise AccessDenied('You don\'t have set support permission !')
        return super().has_object_permission(request, view, obj)