from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

def init_contract_permission():
    sale_group = Group.objects.get(name='Sale Group')
    support_group = Group.objects.get(name='Support Group')
    manage_group = Group.objects.get(name='Manage Group')
    current_permission = Permission.objects.get(codename='view_contract')
    for user_group in [sale_group, support_group, manage_group]:
        if current_permission not in user_group.permissions.all():
            user_group.permissions.add(current_permission)
    for permission_type in ['add', 'change']:
        current_permission = Permission.objects.get(codename=f'{permission_type}_contract')
        if current_permission not in sale_group.permissions.all():
            sale_group.permissions.add(current_permission)

class Command(BaseCommand):

    help = 'Initialize permissions on Contracts for bases groups !'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        init_contract_permission()
        self.stdout.write(self.style.SUCCESS('All Done !'))
    
