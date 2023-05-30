# Generated by Django 4.1.7 on 2023-05-29 11:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0002_posts_tags11"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="posts",
            name="tags11",
        ),
        migrations.RemoveField(
            model_name="posts",
            name="tags",
        ),
        migrations.AddField(
            model_name="posts",
            name="tags",
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
