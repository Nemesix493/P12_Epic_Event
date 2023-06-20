from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

def init_company_permission():
    sale_group = Group.objects.get(name='Sale Group')
    sale_group_all_parmissions = sale_group.permissions.all()
    for permission_type in ['add', 'view', 'change'] :
        for model_name in ['prospect', 'client']:
            current_permission = Permission.objects.get(codename=f'{permission_type}_{model_name}')
            if current_permission not in sale_group_all_parmissions:
                sale_group.permissions.add(current_permission)

class Command(BaseCommand):

    help = 'Initialize on Clients for bases groups !'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        init_company_permission()
        self.stdout.write(self.style.SUCCESS('All Done !'))
    
