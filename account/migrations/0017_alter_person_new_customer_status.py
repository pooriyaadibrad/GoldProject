# Generated by Django 5.0.6 on 2024-11-03 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_person_new_customer_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='new_customer_status',
            field=models.BooleanField(default=True),
        ),
    ]
