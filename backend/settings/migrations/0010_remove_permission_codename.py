# Generated by Django 5.1.1 on 2024-11-20 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0009_permission_codename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permission',
            name='codename',
        ),
    ]