import pytest

from phonebook.contacts.models import Contact, PhoneNumber
from phonebook.contacts.services import create_contact, create_phone_number, delete_phone_number, update_contact
from phonebook.contacts.tests.factories import ContactFactory
from phonebook.contacts.tests.helpers import get_random_country_code


@pytest.fixture
def contact(db) -> Contact:
    return ContactFactory()


def test_create_contact(db):
    contact = create_contact(name="Test Contact", phone_number="1234567890")
    assert contact.name == "Test Contact"
    assert contact.phone_number == "1234567890"


def test_update_contact(db, contact: Contact):
    update_contact(contact.id, name="Updated Contact", phone_number="0987654321")
    contact.refresh_from_db()
    assert contact.name == "Updated Contact"
    assert contact.phone_number == "0987654321"


def test_create_contact_with_invalid_number(db):
    with pytest.raises(ValueError):
        create_contact(name="Test Contact", phone_number="1234567890a")


def test_create_contact_with_invalid_country_code(db):
    with pytest.raises(ValueError):
        create_phone_number(contact=contact, number="0987654321", country_code="12345")


def test_create_contact_with_existing_name(db, contact: Contact):
    with pytest.raises(ValueError):
        create_contact(name=contact.name, phone_number="1234567890")


def test_update_contact_with_invalid_number(db, contact: Contact):
    with pytest.raises(ValueError):
        update_contact(contact.id, name="Updated Contact", phone_number="0987654321a")


def test_update_contact_with_invalid_country_code(db, contact: Contact):
    with pytest.raises(ValueError):
        create_phone_number(contact=contact, number="0987654321", country_code="12345")


def test_update_contact_with_existing_name(db, contact: Contact):
    with pytest.raises(ValueError):
        update_contact(contact.id, name=contact.name, phone_number="0987654321")


def test_delete_phone_number(db, contact: Contact):
    # To test the delete_phone_number function,
    # we need to create a more than one phone number because contacts must have at least one phone number.
    phone_number = create_phone_number(contact=contact, number="0987654321", country_code=get_random_country_code())
    phone_number2 = create_phone_number(contact=contact, number="1234567890", country_code=get_random_country_code())
    contact.refresh_from_db()
    assert contact.phone_numbers.count() == 2
    contact = delete_phone_number(pk=phone_number.id)
    assert contact.phone_numbers.count() == 1
    assert contact.phone_numbers.first().id == phone_number2.id


def test_create_phone_number(db, contact: Contact):
    country_code = get_random_country_code()
    phone_number = create_phone_number(contact=contact, number="0987654321", country_code=country_code)
    assert phone_number.number == "0987654321"
    assert phone_number.country_code == country_code
    assert phone_number.contact.id == contact.id
    assert isinstance(phone_number, PhoneNumber)


def test_delete_last_phone_number(db, contact: Contact):
    with pytest.raises(ValueError):
        delete_phone_number(pk=contact.phone_numbers.first().id)
