# Generated by Django 4.2.4 on 2023-09-10 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('origin', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OriginEmailStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_sent', models.BooleanField(default=False)),
                ('generatedLink', models.CharField(default=None, max_length=255, null=True)),
                ('email', models.EmailField(default=None, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('meeting', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='src.meeting')),
            ],
        ),
    ]
