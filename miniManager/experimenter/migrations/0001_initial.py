# Generated by Django 3.2.6 on 2021-10-02 13:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configurator', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.CharField(default='WAITING', max_length=50)),
                ('version', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configurator.version')),
            ],
            options={
                'db_table': 'Round',
            },
        ),
    ]
