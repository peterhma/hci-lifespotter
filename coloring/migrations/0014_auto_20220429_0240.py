# Generated by Django 3.1.5 on 2022-04-29 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coloring', '0013_auto_20220429_0226'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sighting',
            name='time',
            field=models.TimeField(default='02:40:46'),
        ),
    ]