# Generated by Django 5.0.7 on 2024-07-27 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("challenge", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="challenge",
            name="regexp",
            field=models.BooleanField(default=False),
        ),
    ]
