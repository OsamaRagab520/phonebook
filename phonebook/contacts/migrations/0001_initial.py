# Generated by Django 4.2.10 on 2024-02-08 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Contact",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CountryCode",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("code", models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name="PhoneNumber",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.CharField(max_length=20)),
                ("contact", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contacts.contact")),
                (
                    "country_code",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="contacts.countrycode"),
                ),
            ],
        ),
    ]