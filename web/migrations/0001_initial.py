# Generated by Django 3.2.9 on 2022-02-10 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('phoneNumber', models.CharField(max_length=16)),
                ('email', models.TextField(max_length=128)),
                ('additional', models.TextField()),
                ('status', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('fullname', models.CharField(max_length=128)),
                ('role', models.CharField(max_length=16)),
            ],
        ),
    ]