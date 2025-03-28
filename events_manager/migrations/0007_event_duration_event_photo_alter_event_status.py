# Generated by Django 5.1 on 2024-08-27 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events_manager', '0006_alter_eventmaster_end_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duration',
            field=models.PositiveIntegerField(default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='events/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='status',
            field=models.CharField(choices=[('aberto', 'Aberto'), ('pendente', 'Pendente'), ('encerrado', 'Encerrado')], default='aberto', max_length=10),
        ),
    ]
