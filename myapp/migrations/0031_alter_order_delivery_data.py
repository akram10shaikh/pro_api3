# Generated by Django 5.1.1 on 2024-11-15 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0030_restaurantname_labels_restaurantname_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_data',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
