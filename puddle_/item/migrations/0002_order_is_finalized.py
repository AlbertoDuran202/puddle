# Generated by Django 4.2 on 2023-11-24 19:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("item", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="is_finalized",
            field=models.BooleanField(default=False),
        ),
    ]
