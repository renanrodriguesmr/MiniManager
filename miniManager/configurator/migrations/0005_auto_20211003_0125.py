# Generated by Django 3.2.6 on 2021-10-03 01:18

from django.db import migrations

def insert_measure_catalog(apps, schema_editor):
    measures = [
        {"name": "ping", "unit": ""}
    ]

    Measure = apps.get_model("configurator", "PerformanceMeasure")
    for measure in measures:
        catalogItem = Measure(**measure)
        catalogItem.save()

class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0004_auto_20211003_0125'),
    ]

    operations = [
        migrations.RunPython(insert_measure_catalog)
    ]
