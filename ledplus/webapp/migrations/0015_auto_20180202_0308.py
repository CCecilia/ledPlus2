# Generated by Django 2.0.1 on 2018-02-02 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0014_auto_20180201_0420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleled',
            name='ceiling_height',
            field=models.IntegerField(choices=[(1, 'Over 16`'), (2, '12` to 16`'), (3, 'Up to 12`')], default=2),
        ),
    ]
