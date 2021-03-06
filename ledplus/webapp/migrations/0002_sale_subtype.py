# Generated by Django 2.0.1 on 2018-01-30 02:54

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('renewal', models.BooleanField(default=False)),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_authorized_representative', models.CharField(blank=True, max_length=255, null=True)),
                ('service_address', models.CharField(blank=True, max_length=255, null=True)),
                ('service_city', models.CharField(blank=True, max_length=255, null=True)),
                ('service_state', models.CharField(blank=True, max_length=255, null=True)),
                ('service_zip_code', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_subtype', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('sunday', models.IntegerField(default=0)),
                ('monday', models.IntegerField(default=0)),
                ('tuesday', models.IntegerField(default=0)),
                ('wednesday', models.IntegerField(default=0)),
                ('thursday', models.IntegerField(default=0)),
                ('friday', models.IntegerField(default=0)),
                ('saturday', models.IntegerField(default=0)),
                ('total_hours_of_operation', models.IntegerField(default=0)),
            ],
        ),
    ]
