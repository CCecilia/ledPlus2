# Generated by Django 2.0.1 on 2018-01-30 21:01

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20180130_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='led',
            name='ballast',
            field=models.CharField(choices=[('Electronic', 'Electronic'), ('Magnetic', 'Magnetic')], default='Electronic', max_length=20),
        ),
        migrations.AlterField(
            model_name='led',
            name='brands',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('Philips', 'Philips'), ('Forest', 'Forest'), ('ELB', 'ELB'), ('Satco', 'Satco'), ('Sylvania', 'Sylvania'), ('n/a', 'n/a'), ('Way to Go', 'Way to Go'), ('Green Creative', 'Green Creative'), ('LED Plus', 'LED Plus')], default='Philips', max_length=71),
        ),
        migrations.AlterField(
            model_name='led',
            name='colors',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('5000K', '5000K'), ('2700K', '2700K')], default='5000K', max_length=11),
        ),
        migrations.AlterField(
            model_name='led',
            name='type',
            field=models.CharField(choices=[('Tube', 'Tube'), ('U-BEND Tube', 'U-BEND Tube'), ('Lamp', 'Lamp'), ('Candelabra', 'Candelabra'), ('Spot', 'Spot'), ('Flood', 'Flood'), ('Track', 'Track'), ('4 pin', '4 pin'), ('Fixture', 'Fixture')], default='Tube', max_length=20),
        ),
    ]
