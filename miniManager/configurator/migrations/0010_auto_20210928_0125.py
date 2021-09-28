# Generated by Django 3.2.6 on 2021-09-28 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configurator', '0009_auto_20210927_2126'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accesspoint',
            old_name='modo',
            new_name='mode',
        ),
        migrations.RenameField(
            model_name='interface',
            old_name='fixo',
            new_name='fixed',
        ),
        migrations.RenameField(
            model_name='link',
            old_name='conexao',
            new_name='connection',
        ),
        migrations.RenameField(
            model_name='link',
            old_name='fixo',
            new_name='fixed',
        ),
        migrations.RenameField(
            model_name='link',
            old_name='tamanho_maximo_fila',
            new_name='max_queue_size',
        ),
        migrations.RenameField(
            model_name='mobility',
            old_name='fixo',
            new_name='fixed',
        ),
        migrations.RenameField(
            model_name='network',
            old_name='fixo',
            new_name='fixed',
        ),
        migrations.RenameField(
            model_name='node',
            old_name='fixo',
            new_name='fixed',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='start_time',
        ),
        migrations.AlterField(
            model_name='configuration',
            name='stop_time',
            field=models.IntegerField(null=True),
        ),
    ]