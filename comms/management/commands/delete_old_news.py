"""
Management command: delete_old_news
------------------------------------
Deletes News posts (Post records WITHOUT linked Event) that are older than 4 months.
Event posts are intentionally preserved regardless of age.

Usage:
    python manage.py delete_old_news
    python manage.py delete_old_news --dry-run   # preview without deleting
"""

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from comms.models import Post


class Command(BaseCommand):
    help = 'Delete news posts older than 4 months (events are not affected).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting.',
        )

    def handle(self, *args, **options):
        cutoff = timezone.now() - timedelta(days=4 * 30)
        # Only plain news posts – exclude Posts that have an Event attached
        old_news = Post.objects.filter(
            created_at__lt=cutoff,
            event_details__isnull=True,
        )
        count = old_news.count()

        if options['dry_run']:
            self.stdout.write(
                self.style.WARNING(
                    f'[DRY-RUN] {count} news post(s) would be deleted (older than {cutoff.date()}).'
                )
            )
            for post in old_news:
                self.stdout.write(f'  - [{post.created_at.date()}] {post.title}')
            return

        old_news.delete()
        self.stdout.write(
            self.style.SUCCESS(f'Deleted {count} news post(s) older than {cutoff.date()}.')
        )
