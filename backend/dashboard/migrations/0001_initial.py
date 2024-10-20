# Generated by Django 5.1.1 on 2024-10-20 09:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zabbix_server_url', models.CharField(default='localhost', max_length=255)),
                ('zabbix_username', models.CharField(default='Admin', max_length=255)),
                ('zabbix_password', models.CharField(default='zabbix', max_length=255)),
                ('zabbix_host_name', models.CharField(default='Zabbix server', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
