# Generated by Django 3.2.4 on 2021-09-26 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('room_access_manager', '0002_rename_doors_door'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Door',
            new_name='DoorAccess',
        ),
    ]
