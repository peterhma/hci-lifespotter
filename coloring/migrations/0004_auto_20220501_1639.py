# Generated by Django 3.1.5 on 2022-05-01 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coloring', '0003_auto_20220501_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sighting',
            name='image',
            field=models.ImageField(default='default.jpg', null=True, upload_to='images'),
        ),
        migrations.AlterField(
            model_name='sighting',
            name='time',
            field=models.TimeField(default='16:39:31'),
        ),
    ]