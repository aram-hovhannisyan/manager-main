# Generated by Django 4.2 on 2023-06-25 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0027_usertable_singletable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='debt',
            name='is_return',
        ),
        migrations.RemoveField(
            model_name='debt',
            name='supplier',
        ),
        migrations.AddField(
            model_name='debt',
            name='joined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='debt',
            name='single',
            field=models.BooleanField(default=False),
        ),
    ]