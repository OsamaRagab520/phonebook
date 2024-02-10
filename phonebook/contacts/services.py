from django.db import transaction
from django.shortcuts import get_object_or_404

from phonebook.contacts.models import Contact, CountryCode, PhoneNumber
from phonebook.contacts.selectors import get_contact


def create_phone_number(*, contact: Contact, country_code: str, number: str):
    if not number.isdigit():
        raise ValueError("Number must be numeric")

    try:
        country_code = CountryCode.objects.get(code=country_code)
    except CountryCode.DoesNotExist:
        raise ValueError("Country code does not exist")
    except CountryCode.MultipleObjectsReturned:
        country_code = CountryCode.objects.filter(code=country_code).first()

    return PhoneNumber.objects.create(contact=contact, country_code=country_code, number=number)


def delete_phone_number(*, pk: int) -> Contact:
    phone_number = get_object_or_404(PhoneNumber, pk=pk)

    if phone_number.contact.phone_numbers.count() == 1:
        raise ValueError("Contact must have at least one phone number")

    phone_number.delete()
    return phone_number.contact


@transaction.atomic
def create_contact(*, name: str, numbers: list[str], codes: list[str]):
    if Contact.objects.filter(name=name).exists():
        raise ValueError("Contact with this name already exists")

    contact = Contact(name=name)
    contact.full_clean()
    contact.save()

    for number, code in zip(numbers, codes):
        create_phone_number(contact=contact, country_code=code, number=number)
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
        create_phone_number(contact=contact, country_code=code, number=number)

    return contact
