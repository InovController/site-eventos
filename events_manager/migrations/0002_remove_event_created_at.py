# Generated by Django 5.1 on 2024-08-22 19:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events_manager', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='created_at',
        ),
    ]
