# Generated by Django 5.1.6 on 2025-03-20 06:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avia', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='airports',
            old_name='main',
            new_name='aero',
        ),
    ]
