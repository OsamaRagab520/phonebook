from django.db import migrations
from django.core.management import call_command

def populate_country_codes(apps, schema_editor):
    call_command('populate_country_codes')

class Migration(migrations.Migration):

    dependencies = [
        ("contacts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_country_codes)
    ]
