# Generated by Django 3.2.2 on 2021-05-19 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MusicBeats', '0007_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='image',
            field=models.CharField(default='', max_length=10000000),
        ),
    ]
