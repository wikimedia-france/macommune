# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-20 09:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Communes',
            fields=[
                ('qid', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('wp_title', models.CharField(max_length=255)),
                ('wv_title', models.CharField(max_length=255)),
                ('commons_category', models.CharField(max_length=255)),
                ('suggest_str', models.CharField(max_length=255)),
                ('insee', models.CharField(max_length=16)),
                ('population', models.IntegerField(blank=True, null=True)),
                ('badge', models.CharField(blank=True, max_length=20, null=True)),
                ('progress', models.CharField(blank=True, max_length=20, null=True)),
                ('importance', models.CharField(blank=True, max_length=20, null=True)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('geoshape', models.TextField()),
                ('section_geography', models.IntegerField()),
                ('section_history', models.IntegerField()),
                ('section_economy', models.IntegerField()),
                ('section_demographics', models.IntegerField()),
                ('section_etymology', models.IntegerField()),
                ('section_governance', models.IntegerField()),
                ('section_culture', models.IntegerField()),
                ('section_infrastructure', models.IntegerField()),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('size', models.IntegerField()),
                ('has_sub_article', models.IntegerField()),
                ('qid', models.ForeignKey(blank=True, db_column='qid', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='mc_frontend.Communes')),
            ],
        ),
        migrations.AddIndex(
            model_name='communes',
            index=models.Index(fields=['qid'], name='mc_frontend_qid_1b2ece_idx'),
        ),
        migrations.AddIndex(
            model_name='communes',
            index=models.Index(fields=['suggest_str'], name='mc_frontend_suggest_9b79c1_idx'),
        ),
        migrations.AddIndex(
            model_name='communes',
            index=models.Index(fields=['latitude', 'longitude'], name='mc_frontend_latitud_97cb86_idx'),
        ),
    ]
