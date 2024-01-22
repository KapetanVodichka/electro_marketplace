from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        superuser = User.objects.create(email='admin', is_staff=True, is_active=True, is_superuser=True)
        superuser.set_password('admin')
        superuser.save()
