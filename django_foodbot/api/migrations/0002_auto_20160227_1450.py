# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'ordering': ('-created_at',)},
        ),
        migrations.RenameField(
            model_name='rating',
            old_name='date',
            new_name='created_at',
        ),
    ]
