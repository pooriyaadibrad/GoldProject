# Generated by Django 5.0.6 on 2024-08-01 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0027_alter_buyrequst_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convertgoldrequst',
            name='gold',
            field=models.DecimalField(decimal_places=6, max_digits=8),
        ),
    ]
