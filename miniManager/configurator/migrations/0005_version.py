# Generated by Django 3.2.6 on 2021-09-26 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0004_auto_20210921_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'Version',
            },
        ),
    ]