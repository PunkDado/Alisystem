# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-07-01 20:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Alisystem', '0007_atendimento_verificado'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='atendimento',
            options={'ordering': ['-data_atendimento']},
        ),
        migrations.AlterModelOptions(
            name='procedimentos_aplicado',
            options={},
        ),
        migrations.AlterField(
            model_name='atendimento',
            name='verificado',
            field=models.BooleanField(default=False, help_text='Atendimento verificado pela administração do consultório', verbose_name='Atendimento verificado'),
        ),
    ]
