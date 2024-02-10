from django.db.models.query import QuerySet

from phonebook.common.utils import get_object
from phonebook.contacts.models import Contact, CountryCode


def list_country_codes() -> QuerySet[CountryCode]:
    return CountryCode.objects.all()


def list_contacts() -> QuerySet[Contact]:
    return Contact.objects.all()


def get_contact(*, pk: int) -> Contact | None:
    return get_object(Contact, pk=pk)


def get_contacts_by_name(name: str) -> QuerySet[Contact]:
    return Contact.objects.filter(name__icontains=name)
