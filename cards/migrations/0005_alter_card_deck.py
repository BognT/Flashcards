# Generated by Django 5.0.6 on 2024-06-20 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_deck_card_deck'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='deck',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='cards.deck'),
        ),
    ]