# Generated by Django 5.1 on 2025-03-27 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_manager', '0017_alter_event_departament_delete_eventdepartament'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
