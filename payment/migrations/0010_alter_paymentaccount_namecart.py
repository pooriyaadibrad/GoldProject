# Generated by Django 5.0.6 on 2024-07-19 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_alter_paymentaccount_namecart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentaccount',
            name='nameCart',
            field=models.CharField(max_length=100, null=True),
        ),
    ]