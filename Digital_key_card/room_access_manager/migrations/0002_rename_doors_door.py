# Generated by Django 3.2.4 on 2021-09-26 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_access_manager', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='doors',
            new_name='Door',
        ),
    ]
