# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-16 03:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('EGEbot', '0002_auto_20170415_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='')),
                ('file_id', models.CharField(blank=True, default='', max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.SmallIntegerField()),
                ('text', models.TextField()),
                ('answer', models.CharField(max_length=64)),
                ('photo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='EGEbot.Photo')),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.SmallIntegerField(default=-1),
        ),
        migrations.AddField(
            model_name='user',
            name='current_task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='EGEbot.Task'),
        ),
    ]
