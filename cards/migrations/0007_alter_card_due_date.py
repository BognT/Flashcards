# Generated by Django 5.0.6 on 2024-06-27 10:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0006_card_due_date_card_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]