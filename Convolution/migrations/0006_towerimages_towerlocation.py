# Generated by Django 3.2.3 on 2021-08-04 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Convolution', '0005_towerimages'),
    ]

    operations = [
        migrations.AddField(
            model_name='towerimages',
            name='towerlocation',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
