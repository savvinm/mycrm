# Generated by Django 3.2.9 on 2022-02-10 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='deadline',
        ),
    ]
