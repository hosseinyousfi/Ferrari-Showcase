# Generated by Django 5.0.1 on 2024-09-14 03:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ferrari", "0016_rename_client_shopping_cart"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shopping_cart",
            name="cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="ferrari.ferrari_car"
            ),
        ),
    ]
