# Generated by Django 5.0.6 on 2024-11-03 14:48

import django_jalali.db.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0037_alter_paymentaccount_goldinventory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getgoldrequst',
            name='date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date',
            field=django_jalali.db.models.jDateTimeField(auto_now_add=True),
        ),
    ]