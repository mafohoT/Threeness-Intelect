# Generated by Django 3.2.7 on 2021-10-10 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0045_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin',
            name='appointment_reason',
        ),
    ]
