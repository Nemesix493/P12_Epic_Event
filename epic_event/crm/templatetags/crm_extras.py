from django.template import Library
from django.contrib.auth.models import Permission

register = Library()

@register.filter
def has_set_support_permission(user):
    set_support_permission = Permission.objects.get(codename='set_support_event')
    set_support_permission_natural_key = Permission.objects.get(codename='set_support_event').natural_key()
    return user.has_perm(f'{set_support_permission_natural_key[1]}.{set_support_permission_natural_key[0]}')