from phonebook.contacts.models import CountryCode


def get_random_country_code() -> CountryCode:
    return CountryCode.objects.order_by("?").first()
