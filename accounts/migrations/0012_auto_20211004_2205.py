# Generated by Django 3.2.7 on 2021-10-04 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20211004_2104'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='Doctor',
            new_name='doctor',
        ),
        migrations.RenameField(
            model_name='appointment',
            old_name='Patient',
            new_name='patient',
        ),
    ]
