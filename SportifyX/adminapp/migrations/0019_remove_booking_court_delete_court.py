# Generated by Django 5.1.6 on 2025-03-18 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0018_court_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='court',
        ),
        migrations.DeleteModel(
            name='Court',
        ),
    ]
