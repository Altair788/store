from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@medvs.ru',
            first_name='Admin',
            last_name='Medvs',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('lsudfghsduifgskdfghskfg98475medvs')
        user.save()
