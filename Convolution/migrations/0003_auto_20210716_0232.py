# Generated by Django 3.2.3 on 2021-07-16 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Convolution', '0002_auto_20210716_0206'),
    ]

    operations = [
        migrations.RenameField(
            model_name='corridorline',
            old_name='destination_coordinate',
            new_name='source_coordinate_lat',
        ),
        migrations.RenameField(
            model_name='corridorline',
            old_name='source_coordinate',
            new_name='source_coordinate_long',
        ),
        migrations.AddField(
            model_name='corridorline',
            name='destination_coordinate_lat',
            field=models.FloatField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='corridorline',
            name='destination_coordinate_long',
            field=models.FloatField(max_length=200, null=True),
        ),
    ]
