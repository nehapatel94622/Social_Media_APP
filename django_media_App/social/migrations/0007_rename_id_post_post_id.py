# Generated by Django 4.1.3 on 2022-11-23 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_alter_post_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='id',
            new_name='post_id',
        ),
    ]