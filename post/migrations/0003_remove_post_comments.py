# Generated by Django 3.2.9 on 2021-12-09 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='comments',
        ),
    ]
