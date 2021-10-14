# Generated by Django 3.2.6 on 2021-09-26 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0005_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'TestPlan',
            },
        ),
        migrations.AddField(
            model_name='version',
            name='test_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configurator.testplan'),
        ),
    ]