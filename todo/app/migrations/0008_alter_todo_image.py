# Generated by Django 4.1.4 on 2022-12-21 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_mycustommodel_first_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='image',
            field=models.ImageField(max_length=255, null=True, upload_to='picture'),
        ),
    ]
