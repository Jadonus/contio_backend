# Generated by Django 4.2.4 on 2023-09-10 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='name',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='origin',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
