from phonebook.contacts.models import CountryCode


def get_random_country_code() -> CountryCode:
    country_code = CountryCode.objects.order_by("?").first()
    if country_code is None:
        raise ValueError("country codes not populated in db yet")
    return country_code
