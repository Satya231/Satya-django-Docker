# Generated by Django 4.1.4 on 2022-12-13 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_group_chat'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Chat',
        ),
        migrations.DeleteModel(
            name='Group',
        ),
    ]
