from django.shortcuts import get_object_or_404, redirect, render

from phonebook.contacts.models import Contact, CountryCode
from phonebook.contacts.services import (
    create_contact,
    delete_phone_number,
    get_contact,
    list_contacts,
    list_country_codes,
    update_contact,
)


def add_contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        numbers = request.POST.getlist("numbers[]")
        codes = request.POST.getlist("codes[]")
        create_contact(name=name, numbers=numbers, codes=codes)
        return redirect("contacts:contact_list")
    else:
        country_codes = list_country_codes()
        return render(request, "contacts/add_contact.html", {"country_codes": country_codes})


def contact_list(request):
    contacts = list_contacts()
    return render(request, "contacts/contact_list.html", {"contacts": contacts})


def contact_detail(request, pk):
    contact = get_contact(pk=pk)
    return render(request, "contacts/contact_detail.html", {"contact": contact})


def delete_contact(request, pk):
    contact = get_contact(pk=pk)
    contact.delete()
    return redirect("contacts:contact_list")


def edit_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == "POST":
        name = request.POST["name"]
        numbers = request.POST.getlist("numbers[]")
        codes = request.POST.getlist("codes[]")
        update_contact(name=name, numbers=numbers, codes=codes)
        return redirect("contacts:contact_list")
    else:
        country_codes = CountryCode.objects.all()
        return render(request, "contacts/edit_contact.html", {"contact": contact, "country_codes": country_codes})


def delete_phone(request, pk):
    contact = delete_phone_number(pk=pk)
    return redirect("contacts:contact_detail", pk=contact.pk)
