# Generated by Django 5.0.7 on 2024-07-27 06:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Challenge",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=250)),
                ("description", models.TextField(blank=True, null=True)),
                ("score", models.IntegerField()),
                ("flag", models.CharField(blank=True, max_length=250, null=True)),
                ("active", models.BooleanField(default=True)),
                ("team", models.BooleanField(default=False)),
                ("hidden", models.BooleanField(default=False)),
                ("dynamic", models.BooleanField(default=False)),
                ("start", models.DateTimeField(blank=True, null=True)),
                ("end", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("correct", models.BooleanField()),
                ("flag", models.CharField(blank=True, max_length=250, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("challenge", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="challenge.challenge")),
            ],
        ),
    ]
