# Generated by Django 5.1.1 on 2024-09-12 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ferrari", "0012_passwordreset"),
    ]

    operations = [
        migrations.DeleteModel(
            name="PasswordReset",
        ),
    ]
