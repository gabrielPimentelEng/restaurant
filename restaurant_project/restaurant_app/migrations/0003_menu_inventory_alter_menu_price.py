# Generated by Django 5.0.4 on 2024-04-25 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant_app', '0002_menu_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='inventory',
            field=models.SmallIntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='menu',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
