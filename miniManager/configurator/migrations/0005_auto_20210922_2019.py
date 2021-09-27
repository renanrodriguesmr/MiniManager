# Generated by Django 3.2.6 on 2021-09-22 20:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0004_auto_20210921_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='PModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'PModel',
            },
        ),
        migrations.CreateModel(
            name='PropagationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurator.pmodel')),
            ],
            options={
                'db_table': 'PropagationModel',
            },
        ),
        migrations.CreateModel(
            name='PropagationParam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('value', models.FloatField()),
                ('propagationmodel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configurator.propagationmodel')),
            ],
            options={
                'db_table': 'PropagationParam',
            },
        ),
        migrations.AddField(
            model_name='configuration',
            name='propagationmodel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='configurator.propagationmodel'),
        ),
    ]
