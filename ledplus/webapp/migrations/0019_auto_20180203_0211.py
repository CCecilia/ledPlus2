# Generated by Django 2.0.1 on 2018-02-03 02:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0018_auto_20180202_2258'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConsumptionScaler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=2)),
                ('JAN', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('FEB', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('MAR', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('APR', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('MAY', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('JUN', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('JUL', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('AUG', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('SEP', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('OCT', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('NOV', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('DEC', models.DecimalField(decimal_places=4, default=0.0, max_digits=6)),
                ('service_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.ServiceClass')),
                ('utility', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.Utility')),
                ('zone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='webapp.Zone')),
            ],
        ),
        migrations.RemoveField(
            model_name='rate',
            name='retail_energy_provider',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='service_class',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='team',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='utility',
        ),
        migrations.RemoveField(
            model_name='rate',
            name='zone',
        ),
        migrations.DeleteModel(
            name='Rate',
        ),
    ]
