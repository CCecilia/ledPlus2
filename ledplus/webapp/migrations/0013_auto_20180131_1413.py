# Generated by Django 2.0.1 on 2018-01-31 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0012_auto_20180131_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('active', models.BooleanField(default=False)),
            ],
        ),
        migrations.AlterField(
            model_name='utility',
            name='state',
            field=models.CharField(max_length=2),
        ),
    ]
