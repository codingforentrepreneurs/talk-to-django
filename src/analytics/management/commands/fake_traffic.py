import random
from django.core.management.base import BaseCommand
from django.db import transaction
from analytics.models import PageView
from blog.models import BlogPost
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = "Generate random page views for blog posts"

    def add_arguments(self, parser):
        parser.add_argument('--min', type=int, default=500, help='Minimum number of views')
        parser.add_argument('--max', type=int, default=2500, help='Maximum number of views')

    def handle(self, *args, **options):
        min_views = options['min']
        max_views = options['max']

        with transaction.atomic():
            qs = BlogPost.objects.filter(can_delete=True)
            total_views = 0

            for obj in qs:
                rand_views = random.randint(min_views, max_views)
                page_views = []
                now = timezone.now()

                for _ in range(rand_views):
                    random_time = now - timedelta(days=random.randint(0, 30))
                    page_views.append(
                        PageView(post=obj, timestamp=random_time)
                    )

                PageView.objects.bulk_create(page_views)
                total_views += rand_views

            self.stdout.write(self.style.SUCCESS(f"Random views completed. Total views added: {total_views}"))