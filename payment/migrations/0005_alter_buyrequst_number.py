# Generated by Django 5.0.6 on 2024-07-18 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_remove_paymentaccount_endurance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyrequst',
            name='number',
            field=models.CharField(max_length=16),
        ),
    ]
