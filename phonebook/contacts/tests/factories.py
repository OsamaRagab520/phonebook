from factory import LazyAttribute, SubFactory
from factory.django import DjangoModelFactory

from phonebook.contacts.models import Contact, PhoneNumber
from phonebook.contacts.tests.helpers import get_random_country_code
from phonebook.utils.tests.base import faker


class ContactFactory(DjangoModelFactory):
    name = LazyAttribute(lambda _: faker.name())
    created_at = LazyAttribute(lambda _: faker.date_time_this_month())

    class Meta:
        model = Contact


class PhoneNumberFactory(DjangoModelFactory):
    contact = SubFactory(ContactFactory)
    country_code = LazyAttribute(lambda _: get_random_country_code())
    number = LazyAttribute(lambda _: faker.phone_number())

    class Meta:
        model = PhoneNumber


# No need to create a factory for CountryCode because it's prepopulated with data by the migrations.
#  we can just use the get_random_country_code function from the helpers module.
