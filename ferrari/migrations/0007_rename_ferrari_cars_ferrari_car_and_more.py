# Generated by Django 5.1.1 on 2024-09-10 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ferrari", "0006_alter_ferrari_models_model_desciption"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Ferrari_cars",
            new_name="Ferrari_car",
        ),
        migrations.RenameModel(
            old_name="Ferrari_models",
            new_name="Ferrari_model",
        ),
    ]
