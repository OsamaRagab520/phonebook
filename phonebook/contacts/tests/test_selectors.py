from phonebook.contacts.models import Contact
from phonebook.contacts.selectors import get_contact, get_contacts_by_name, list_contacts
from phonebook.contacts.tests.factories import ContactFactory


def test_list_contacts(db):
    ContactFactory.create_batch(5)
    contacts = list_contacts()
    assert len(contacts) == 5


def test_get_contact(db, contact_with_phone_number: Contact):
    contact = contact_with_phone_number
    fetched_contact = get_contact(pk=contact.id)
    assert fetched_contact.id == contact.id
    assert fetched_contact.name == contact.name
    assert fetched_contact.phone_numbers == contact.phone_numbers


def test_get_contacts_by_name(db):
    ContactFactory(name="Test Contact")
    contacts = get_contacts_by_name("Test Contact")
    assert len(contacts) == 1
    assert contacts[0].name == "Test Contact"


def test_get_contacts_by_name_with_no_match(db):
    contacts = get_contacts_by_name("Test Contact")
    assert len(contacts) == 0


def test_get_contacts_by_name_with_partial_match(db):
    ContactFactory(name="Test Contact")
    contacts = get_contacts_by_name("Test")
    assert len(contacts) == 1
    assert contacts[0].name == "Test Contact"


def test_get_contacts_by_name_with_case_insensitive_match(db):
    ContactFactory(name="Test Contact")
    contacts = get_contacts_by_name("test contact")
    assert len(contacts) == 1
    assert contacts[0].name == "Test Contact"


def test_get_contacts_by_name_with_case_insensitive_partial_match(db):
    ContactFactory(name="Test Contact")
    contacts = get_contacts_by_name("test")
    assert len(contacts) == 1
    assert contacts[0].name == "Test Contact"


def test_get_contacts_by_name_with_multiple_matches(db):
    ContactFactory.create_batch(5, name="Test Contact")
    contacts = get_contacts_by_name("Test Contact")
    assert len(contacts) == 5
    for contact in contacts:
        assert contact.name == "Test Contact"


def test_get_contacts_by_name_with_multiple_matches_and_partial_match(db):
    ContactFactory.create_batch(5, name="Test Contact")
    contacts = get_contacts_by_name("Test")
    assert len(contacts) == 5
    for contact in contacts:
        assert contact.name == "Test Contact"


def test_get_contacts_by_name_with_multiple_matches_and_case_insensitive_match(db):
    ContactFactory.create_batch(5, name="Test Contact")
    contacts = get_contacts_by_name("test contact")
    assert len(contacts) == 5
    for contact in contacts:
        assert contact.name == "Test Contact"


def test_get_contacts_by_name_with_multiple_matches_and_case_insensitive_partial_match(db):
    ContactFactory.create_batch(5, name="Test Contact")
    contacts = get_contacts_by_name("test")
    assert len(contacts) == 5
    for contact in contacts:
        assert contact.name == "Test Contact"
