# Generated by Django 4.0.4 on 2022-05-26 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0003_subscription_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='user/<django.db.models.fields.related.ForeignKey>/%Y/%m/%d'),
        ),
    ]
