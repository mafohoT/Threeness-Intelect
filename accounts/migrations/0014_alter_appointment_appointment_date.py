# Generated by Django 3.2.7 on 2021-10-05 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20211005_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateTimeField(null=True),
        ),
    ]