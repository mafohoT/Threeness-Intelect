# Generated by Django 3.2.7 on 2021-10-13 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0048_appointment_doctor'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='id_number',
            field=models.CharField(max_length=13, null=True),
        ),
    ]