from django.apps import AppConfig
from django.core.management import call_command


class ContactsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "phonebook.contacts"

    def ready(self):
        call_command("populate_country_codes")
