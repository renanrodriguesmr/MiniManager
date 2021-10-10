# Generated by Django 3.2.6 on 2021-10-03 01:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0003_auto_20211002_1339'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerformanceMeasure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('unit', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'PerformanceMeasure',
            },
        ),
        migrations.AlterField(
            model_name='network',
            name='fixed',
            field=models.BooleanField(default=True),
        ),
        migrations.CreateModel(
            name='PerformanceMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('period', models.IntegerField()),
                ('source', models.CharField(max_length=20)),
                ('destination', models.CharField(max_length=20)),
                ('config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurator.configuration')),
                ('measure', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurator.performancemeasure')),
            ],
            options={
                'db_table': 'PerformanceMeasurement',
            },
        ),
    ]
