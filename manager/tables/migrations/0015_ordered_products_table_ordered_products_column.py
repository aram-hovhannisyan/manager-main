# Generated by Django 4.2 on 2023-06-08 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tables', '0014_debt_is_return'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ordered_Products_Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nameof_Table', models.CharField(max_length=150)),
                ('dateof_Creating', models.DateTimeField(auto_now=True)),
                ('supplierof_Table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ordered_Products_Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parent_Table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.ordered_products_table')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.usertable')),
            ],
        ),
    ]
