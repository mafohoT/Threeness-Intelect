# Generated by Django 3.2.7 on 2021-10-02 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20211002_1211'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='Name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='Surname',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.AddField(
            model_name='patient',
            name='username',
            field=models.CharField(max_length=20, null=True),
        ),
    ]