# Generated by Django 5.1.5 on 2025-02-10 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0002_alter_venuelist_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuelist',
            name='location',
            field=models.URLField(blank=True, null=True),
        ),
    ]
