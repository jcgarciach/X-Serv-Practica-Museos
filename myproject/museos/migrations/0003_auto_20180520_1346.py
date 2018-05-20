# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos', '0002_auto_20180520_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preferencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('titulo', models.CharField(max_length=50, blank=True)),
                ('tamanioLetra', models.CharField(max_length=50, blank=True)),
                ('colorFondo', models.CharField(max_length=20, blank=True)),
                ('usuario', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fechaHora', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='control',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='seleccionmuseo',
            name='museo',
        ),
        migrations.RemoveField(
            model_name='seleccionmuseo',
            name='usuario',
        ),
        migrations.RenameField(
            model_name='museo',
            old_name='idx',
            new_name='idEntidad',
        ),
        migrations.AddField(
            model_name='museo',
            name='latitud',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='museo',
            name='longitud',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Control',
        ),
        migrations.DeleteModel(
            name='Seleccionmuseo',
        ),
        migrations.AddField(
            model_name='registro',
            name='museo',
            field=models.ForeignKey(to='museos.Museo'),
        ),
        migrations.AddField(
            model_name='registro',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
