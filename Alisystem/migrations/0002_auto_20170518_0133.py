# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-05-18 01:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alisystem', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='procedimentos_aplicado',
            options={'ordering': ['id']},
        ),
        migrations.RemoveField(
            model_name='atendimento',
            name='procedimentos_aplicados',
        ),
        migrations.AddField(
            model_name='atendimento',
            name='procedimentos_aplicados',
            field=models.ManyToManyField(to='Alisystem.Procedimentos_aplicado'),
        ),
    ]
