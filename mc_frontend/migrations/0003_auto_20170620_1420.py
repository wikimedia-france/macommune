# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mc_frontend', '0002_auto_20170620_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='geoloc',
            name='id',
        ),
        migrations.AlterField(
            model_name='communes',
            name='badge',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='communes',
            name='commons_category',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='communes',
            name='importance',
            field=models.CharField(blank=True, default='?', max_length=20),
        ),
        migrations.AlterField(
            model_name='communes',
            name='insee',
            field=models.CharField(default=None, max_length=16, null=True),
        ),
        migrations.AlterField(
            model_name='communes',
            name='population',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='progress',
            field=models.CharField(blank=True, default='?', max_length=20),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_culture',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_demographics',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_economy',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_etymology',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_geography',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_governance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_history',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='section_infrastructure',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='communes',
            name='suggest_str',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='communes',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='communes',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='communes',
            name='wp_title',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='communes',
            name='wv_title',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='geoloc',
            name='qid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='mc_frontend.Communes'),
        ),
    ]
