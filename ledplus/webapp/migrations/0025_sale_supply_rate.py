# Generated by Django 2.0.1 on 2018-02-07 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0024_auto_20180204_0146'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='supply_rate',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=6),
        ),
    ]
