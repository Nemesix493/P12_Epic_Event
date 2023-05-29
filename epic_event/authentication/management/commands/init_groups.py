from django.core.management.base import BaseCommand

from authentication.models import StaffMember
class Command(BaseCommand):

    help = 'Initialize base group for Users Models !'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))
        StaffMember.init_default_groups()
        self.stdout.write(self.style.SUCCESS('All Done !'))