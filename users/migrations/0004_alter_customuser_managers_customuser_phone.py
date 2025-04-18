# Generated by Django 5.1 on 2024-09-05 18:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_company'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone',
            field=models.CharField(default=213, max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='O número de telefone deve estar no formato: (__) 00000-0000.', regex='^\\(\\d{2}\\) \\d{5}-\\d{4}$')]),
            preserve_default=False,
        ),
    ]
