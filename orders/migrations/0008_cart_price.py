# Generated by Django 2.1.5 on 2020-02-05 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='price',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
