# Generated by Django 3.0.8 on 2020-07-13 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200713_1853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follow',
            old_name='follower',
            new_name='following',
        ),
        migrations.RenameField(
            model_name='follow',
            old_name='author',
            new_name='user',
        ),
    ]