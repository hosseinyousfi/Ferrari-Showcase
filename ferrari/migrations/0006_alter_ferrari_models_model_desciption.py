# Generated by Django 5.1.1 on 2024-09-10 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ferrari", "0005_ferrari_models_model_desciption"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ferrari_models",
            name="model_desciption",
            field=models.CharField(default="Ferrari", max_length=200),
        ),
    ]
