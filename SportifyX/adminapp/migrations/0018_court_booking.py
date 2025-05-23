# Generated by Django 5.1.6 on 2025-03-17 07:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0017_notification_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_available', models.BooleanField(default=True)),
                ('game_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courts', to='adminapp.game_category_list')),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courts', to='adminapp.venuelist')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('duration', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('game_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.game_category_list')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.venuelist')),
                ('court', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.court')),
            ],
        ),
    ]
