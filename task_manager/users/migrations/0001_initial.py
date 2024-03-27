# Generated by Django 5.0.3 on 2024-03-15 22:14

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True)),
                ("surname", models.CharField(blank=True)),
                ("nickname", models.CharField(max_length=150)),
                ("password", models.CharField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
