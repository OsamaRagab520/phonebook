import pytest

from phonebook.contacts.models import Contact
from phonebook.contacts.tests.factories import ContactFactory, ContactWithPhoneNumberFactory


@pytest.fixture
def contact(db) -> Contact:
    return ContactFactory()


@pytest.fixture
def contact_with_phone_number(db) -> Contact:
    return ContactWithPhoneNumberFactory()
