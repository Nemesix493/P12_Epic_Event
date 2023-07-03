from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

from authentication.models import StaffMember, ManageMember

def init_groups():
    StaffMember.init_default_groups()
    manage_group = Group.objects.get(name='Manage Group')
    manage_group_all_parmissions = manage_group.permissions.all()
    for permission_type in ['add', 'view', 'change'] :
        for model_name in ['supportmember', 'managemember', 'salemember']:
            current_permission = Permission.objects.get(codename=f'{permission_type}_{model_name}')
            if current_permission not in manage_group_all_parmissions:
                manage_group.permissions.add(current_permission)
    support_group = Group.objects.get(name='Support Group')
    current_permission = Permission.objects.get(codename=f'view_supportmember')
    if current_permission not in support_group.permissions.all():
        support_group.permissions.add(current_permission)
    sale_group = Group.objects.get(name='Sale Group')
    current_permission = Permission.objects.get(codename=f'view_salemember')
    if current_permission not in support_group.permissions.all():
        sale_group.permissions.add(current_permission)

class Command(BaseCommand):

    help = 'Initialize base group for Users Models !'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        init_groups()
        self.stdout.write(self.style.SUCCESS('All Done !'))
