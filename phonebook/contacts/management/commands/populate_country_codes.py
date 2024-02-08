import phonenumbers
import pycountry
from django.core.management.base import BaseCommand

from phonebook.contacts.models import CountryCode


class Command(BaseCommand):
    help = "Populate the CountryCode model with all country codes"

    def handle(self, *args, **options):
        for country in pycountry.countries:
            country_code = phonenumbers.country_code_for_region(country.alpha_2)

            # Some countries don't have a country code
            if country_code != 0:
                CountryCode.objects.get_or_create(name=country.name, code="+" + str(country_code))
