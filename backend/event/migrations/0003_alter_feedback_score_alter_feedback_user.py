# Generated by Django 5.0.7 on 2024-08-03 17:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("event", "0002_feedback"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="feedback",
            name="score",
            field=models.IntegerField(help_text="Score from 1 to 5"),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="user",
            field=models.ForeignKey(
                help_text="User who made the feedback",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="feedbacks",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
