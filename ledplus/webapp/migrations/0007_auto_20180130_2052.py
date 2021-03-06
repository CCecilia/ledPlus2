# Generated by Django 2.0.1 on 2018-01-30 20:52

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_led'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='led',
            name='color',
        ),
        migrations.AlterField(
            model_name='led',
            name='ballast',
            field=models.CharField(choices=[(1, 'Electronic'), (2, 'Magnetic')], default=1, max_length=2),
        ),
        migrations.AlterField(
            model_name='led',
            name='brands',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, 'Philips'), (2, 'Forest'), (3, 'ELB'), (4, 'Satco'), (5, 'Sylvania'), (6, 'n/a'), (7, 'Way to Go'), (8, 'Green Creative'), (9, 'LED Plus')], default=1, max_length=17),
        ),
        migrations.AlterField(
            model_name='led',
            name='colors',
            field=multiselectfield.db.fields.MultiSelectField(choices=[(1, '5000K'), (2, '2700K')], default=1, max_length=3),
        ),
        migrations.AlterField(
            model_name='led',
            name='type',
            field=models.CharField(choices=[(1, 'Tube'), (2, 'U-BEND Tube'), (3, 'Lamp'), (4, 'Candelabra'), (5, 'Spot'), (6, 'Flood'), (7, 'Track'), (8, '4 pin'), (9, 'Fixture')], default=1, max_length=2),
        ),
    ]
