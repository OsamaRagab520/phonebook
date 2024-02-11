from django.db import transaction
from django.shortcuts import get_object_or_404

from phonebook.contacts.models import Contact, CountryCode, PhoneNumber
from phonebook.contacts.selectors import get_contact, get_country_code


def create_phone_number(*, contact: Contact, country_code: CountryCode, number: str):
    if not number.isdigit():
        raise ValueError("Number must be numeric")

    return PhoneNumber.objects.create(contact=contact, country_code=country_code, number=number)


def delete_phone_number(*, pk: int) -> Contact:
    phone_number = get_object_or_404(PhoneNumber, pk=pk)

    if phone_number.contact.phone_numbers.count() == 1:
        raise ValueError("Contact must have at least one phone number")

    phone_number.delete()
    return phone_number.contact


@transaction.atomic
def create_contact(*, name: str, numbers: list[str], codes: list[str]):
    if len(numbers) != len(codes):
        raise ValueError("Number and country code lists must be the same length")

    if Contact.objects.filter(name=name).exists():
        raise ValueError("Contact with this name already exists")

    contact = Contact(name=name)
    contact.full_clean()
    contact.save()

    for number, code in zip(numbers, codes):
        country_code = get_country_code(code=code)
        create_phone_number(contact=contact, country_code=country_code, number=number)
    return contact


@transaction.atomic
def update_contact(*, id: int, name: str, numbers: list[str], codes: list[str]):

    if Contact.objects.exclude(pk=id).filter(name=name).exists():
        raise ValueError("Contact with this name already exists")

    contact = get_contact(pk=id)
    contact.name = name
    contact.phone_numbers.all().delete()

    contact.full_clean()
    contact.save()

    for number, code in zip(numbers, codes):
        country_code = get_country_code(code=code)
        create_phone_number(contact=contact, country_code=country_code, number=number)

    return contact
