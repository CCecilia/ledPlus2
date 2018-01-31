# Generated by Django 2.0.1 on 2018-01-30 15:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_sale_subtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sale',
            name='customer_authorized_representative',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_subtype',
        ),
        migrations.AddField(
            model_name='sale',
            name='authorized_representative',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='business_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sale',
            name='subtype',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='webapp.Subtype'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='service_state',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='subtype',
            name='name',
            field=models.CharField(max_length=254, unique=True),
        ),
    ]
