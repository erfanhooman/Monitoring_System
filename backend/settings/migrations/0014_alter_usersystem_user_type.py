# Generated by Django 5.1.1 on 2024-11-24 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0013_merge_20241124_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersystem',
            name='user_type',
            field=models.CharField(choices=[('admin', 'Admin'), ('user', 'User')], default='user', max_length=20),
        ),
    ]