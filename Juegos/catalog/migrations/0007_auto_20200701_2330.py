# Generated by Django 3.0.7 on 2020-07-01 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_auto_20200701_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique_for_date=True),
        ),
    ]
