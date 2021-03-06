# Generated by Django 2.0.1 on 2018-02-04 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0022_auto_20180204_0111'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale',
            name='energy_only_adder',
            field=models.DecimalField(decimal_places=5, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='sale',
            name='logistics_adder',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='sale',
            name='marketing_adder',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='sale',
            name='max_adder',
            field=models.DecimalField(decimal_places=2, default=0.05, max_digits=3),
        ),
        migrations.AddField(
            model_name='sale',
            name='sales_tax',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=6),
        ),
    ]
