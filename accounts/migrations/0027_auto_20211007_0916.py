# Generated by Django 3.2.7 on 2021-10-07 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20211006_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='appointment_date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='patient',
        ),
    ]
