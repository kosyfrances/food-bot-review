# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('day', models.CharField(max_length=10)),
                ('food', models.TextField()),
                ('meal', models.CharField(max_length=10)),
                ('option', models.IntegerField()),
                ('week', models.IntegerField()),
            ],
            options={
                'ordering': ('-week',),
                'db_table': 'menu_table',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.CharField(max_length=20)),
                ('rate', models.IntegerField()),
                ('comment', models.TextField(default=b'no comment')),
                ('menu', models.ForeignKey(related_name='rating', to='api.Menu')),
            ],
            options={
                'ordering': ('-date',),
                'db_table': 'rating',
            },
        ),
    ]
