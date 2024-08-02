import csv

# pip install dateparser
import dateparser
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import BlogPost

BASE_DIR = settings.BASE_DIR


def parse_date(date_string):
    if not date_string:
        return None
    parsed_date = dateparser.parse(date_string)
    if parsed_date:
        return (
            timezone.make_aware(parsed_date)
            if timezone.is_naive(parsed_date)
            else parsed_date
        )
    return None


class Command(BaseCommand):
    help = "Load blog posts from data.csv file"

    def handle(self, *args, **options):
        with open(
            str(BASE_DIR.parent / "datasets" / "seth-data.csv"), "r", encoding="utf-8"
        ) as file:
            csv_reader = csv.DictReader(file)
            rows = list(csv_reader)
            start_index = max(0, len(rows) - 50)
            for row in rows[start_index:]:
                created_at = parse_date(row["publication-date"])
                if not created_at:
                    # If publication-date is invalid, try to extract from URL
                    created_at = parse_date("/".join(row["url"].split("/")[-4:-2]))

                if not created_at:
                    created_at = timezone.now()

                # Create or update the BlogPost
                BlogPost.objects.update_or_create(
                    title=row["title"],
                    defaults={
                        "content": row["content_plain"],
                        "timestamp": created_at,
                        "can_delete": True
                    },
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully added/updated post: {row['title']} (Date: {created_at})"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Data import completed"))