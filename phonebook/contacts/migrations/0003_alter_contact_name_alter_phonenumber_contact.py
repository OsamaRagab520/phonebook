# Generated by Django 4.2.10 on 2024-02-11 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0002_auto_20240209_1204"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contact",
            name="name",
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name="phonenumber",
            name="contact",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="phone_numbers", to="contacts.contact"
            ),
        ),
    ]
