# Generated by Django 4.1.3 on 2022-11-23 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0007_rename_id_post_post_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_id',
            new_name='id',
        ),
    ]
