# Generated by Django 4.2 on 2023-06-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tables', '0013_suppliersproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='debt',
            name='is_return',
            field=models.BooleanField(default=False, null=True),
        ),
    ]