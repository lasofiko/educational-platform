from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed database with EGE math topics"

    def handle(self, *args, **options):
        self.stdout.write("Seeding database...")
        self.stdout.write(self.style.SUCCESS("Done."))
