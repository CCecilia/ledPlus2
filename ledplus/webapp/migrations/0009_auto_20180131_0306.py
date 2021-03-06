# Generated by Django 2.0.1 on 2018-01-31 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20180130_2101'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaleLed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=254)),
                ('led_count', models.IntegerField(default=0)),
                ('total_count', models.IntegerField(default=0)),
                ('not_replacing_count', models.IntegerField(default=0)),
                ('delampingCount', models.IntegerField(default=0)),
                ('wattageReduction', models.DecimalField(decimal_places=8, default=0, max_digits=16)),
                ('installationRequired', models.BooleanField(default=True)),
                ('ceiling_height', models.CharField(choices=[(1, 'Over 16`'), (2, '12` to 16`'), (3, 'Up to 12`')], default=2, max_length=1)),
                ('recycling', models.BooleanField(default=False)),
                ('led', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='webapp.Led')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='leds',
            field=models.ManyToManyField(to='webapp.SaleLed'),
        ),
    ]
