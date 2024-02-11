import json

from django.core.management.base import BaseCommand

from phonebook.contacts.models import CountryCode


class Command(BaseCommand):
    help = "Populate the CountryCode model with all country codes"

    def handle(self, *args, **options):

        data = json.load(open("phonebook/contacts/data/country_codes.json"))

        for country in data:
            CountryCode.objects.get_or_create(name=country["name"], code=country["dial_code"])
