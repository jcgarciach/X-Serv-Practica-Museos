# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('museos', '0003_auto_20180520_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Select',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('fechaHora', models.DateTimeField()),
                ('museo', models.ForeignKey(to='museos.Museo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='registro',
            name='museo',
        ),
        migrations.RemoveField(
            model_name='registro',
            name='usuario',
        ),
        migrations.DeleteModel(
            name='Registro',
        ),
    ]
