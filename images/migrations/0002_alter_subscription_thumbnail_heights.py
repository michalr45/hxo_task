# Generated by Django 4.0.4 on 2022-05-25 15:53

import django_better_admin_arrayfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='thumbnail_heights',
            field=django_better_admin_arrayfield.models.fields.ArrayField(base_field=models.PositiveIntegerField(), size=None),
        ),
    ]
