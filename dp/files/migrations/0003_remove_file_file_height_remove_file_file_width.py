# Generated by Django 4.0.7 on 2023-07-02 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_file_file_height_file_file_width'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file_height',
        ),
        migrations.RemoveField(
            model_name='file',
            name='file_width',
        ),
    ]
