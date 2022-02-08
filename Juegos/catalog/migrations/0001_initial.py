# Generated by Django 3.0.7 on 2020-07-01 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter category (genre)', max_length=200)),
                ('img_path', models.CharField(default='img/', help_text='Enter path to the image', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Enter a brief description of the game', max_length=1000)),
                ('thumb_path', models.CharField(default='img/', help_text='Enter path to the thumbnail image', max_length=200)),
                ('date_published', models.DateField(default='1990-01-01')),
                ('times_played', models.IntegerField(default=0)),
                ('category', models.ManyToManyField(help_text='Select a category for this game', to='catalog.Category')),
            ],
        ),
    ]
