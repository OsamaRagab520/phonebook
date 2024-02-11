import pytest

from phonebook.contacts.models import Contact, PhoneNumber
from phonebook.contacts.services import create_contact, create_phone_number, delete_phone_number, update_contact
from phonebook.contacts.tests.factories import ContactFactory
from phonebook.contacts.tests.helpers import get_random_country_code


def test_create_contact(db):
    country_code = get_random_country_code()
    test_phone_num = "1234567890"
    contact = create_contact(name="Test Contact", numbers=[test_phone_num], codes=[country_code.code])
    assert contact.name == "Test Contact"
    assert contact.phone_numbers.count() == 1
    assert contact.phone_numbers.first().number == test_phone_num
    assert contact.phone_numbers.first().country_code.code == country_code.code


def test_update_contact(db, contact: Contact):
    country_code = get_random_country_code()
    update_contact(id=contact.id, name="Updated Contact", numbers=["0987654321"], codes=[country_code.code])
    contact.refresh_from_db()
    assert contact.name == "Updated Contact"
    assert contact.phone_numbers.count() == 1
    phone_number = contact.phone_numbers.first()
    if phone_number is None:
        assert False, "Phone number not found"
    assert phone_number.number == "0987654321"
    assert phone_number.country_code == country_code


def test_create_contact_with_invalid_number(db):
    with pytest.raises(ValueError):
        create_contact(name="Test Contact", numbers=["1234567890a"], codes=[get_random_country_code().code])


def test_create_contact_with_existing_name(db, contact: Contact):
    with pytest.raises(ValueError):
        create_contact(name=contact.name, numbers=["1234567890"], codes=[get_random_country_code().code])


def test_update_contact_with_invalid_number(db, contact: Contact):
    with pytest.raises(ValueError):
        update_contact(
            id=contact.id, name="Updated Contact", numbers=["0987654321a"], codes=[get_random_country_code().code]
        )


def test_update_contact_with_existing_name(db, contact: Contact):
    old_contact = ContactFactory()
    with pytest.raises(ValueError):
        update_contact(
            id=contact.id, name=old_contact.name, numbers=["0987654321"], codes=[get_random_country_code().code]
        )


def test_delete_phone_number(db, contact: Contact):
    # To test the delete_phone_number function,
    # we need to create a more than one phone number because contacts must have at least one phone number.
    country_code_1 = get_random_country_code()
    country_code_2 = get_random_country_code()
    phone_number = create_phone_number(contact=contact, number="0987654321", country_code=country_code_1)
    phone_number2 = create_phone_number(contact=contact, number="1234567890", country_code=country_code_2)
    contact.refresh_from_db()
    assert contact.phone_numbers.count() == 2
    contact = delete_phone_number(pk=phone_number.id)
    assert contact.phone_numbers.count() == 1
    remaining_phone_number = contact.phone_numbers.first()
    if remaining_phone_number is None:
        assert False, "Phone number not found"
    assert remaining_phone_number == phone_number2


def test_create_phone_number(db, contact: Contact):
    country_code = get_random_country_code()
    phone_number = create_phone_number(contact=contact, number="0987654321", country_code=country_code)
    assert phone_number.number == "0987654321"
    assert phone_number.country_code == country_code
    assert phone_number.contact.id == contact.id
    assert isinstance(phone_number, PhoneNumber)


def test_delete_last_phone_number(db, contact_with_phone_number: Contact):

    with pytest.raises(ValueError):
        phone_number = contact_with_phone_number.phone_numbers.first()
        if phone_number is None:
            assert False, "Phone number not found"

        delete_phone_number(pk=phone_number.id)


def test_create_contact_with_invalid_country_code(db):
    with pytest.raises(ValueError):
        create_contact(name="Test Contact", numbers=["1234567890"], codes=["123"])


def test_update_contact_with_invalid_country_code(db, contact: Contact):
    with pytest.raises(ValueError):
        update_contact(id=contact.id, name="Updated Contact", numbers=["0987654321"], codes=["123"])
