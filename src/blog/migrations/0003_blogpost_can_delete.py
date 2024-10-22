# Generated by Django 5.0.7 on 2024-07-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0002_blogpost_embedding"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="can_delete",
            field=models.BooleanField(
                default=False, help_text="Use in jupyter notebooks"
            ),
        ),
    ]
