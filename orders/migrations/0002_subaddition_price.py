# Generated by Django 2.1.5 on 2020-01-28 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subaddition',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
