# Generated by Django 2.1.5 on 2020-01-28 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20200128_1030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='meal_size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='sizes', to='orders.MealSize'),
        ),
    ]
