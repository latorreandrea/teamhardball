from django.core.management.base import BaseCommand

from achievements.services import evaluate_all_users_achievements


class Command(BaseCommand):
    help = "Automatic achievement assignment is disabled. This command will not award achievements."

    def handle(self, *args, **options):
        stats = evaluate_all_users_achievements()
        self.stdout.write(
            self.style.SUCCESS(
                f"Achievement evaluation completed. New awards created: {stats.created_count}"
            )
        )
