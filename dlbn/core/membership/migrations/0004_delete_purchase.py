# Generated by Django 4.0.5 on 2023-06-08 02:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0003_remove_subscription_subscription_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Purchase',
        ),
    ]
