# Generated by Django 5.1.1 on 2024-11-12 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_delete_fcmtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='FCMDevice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('device', models.CharField(max_length=300, null=True)),
                ('platform', models.CharField(max_length=300, null=True)),
                ('active', models.BooleanField(default=False)),
                ('fcm_token', models.CharField(max_length=300, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
