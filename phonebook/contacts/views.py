from django.http import Http404
from django.shortcuts import redirect, render

from phonebook.contacts.selectors import list_contacts, list_country_codes
from phonebook.contacts.services import create_contact, delete_phone_number, get_contact, update_contact


def add_contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        numbers = request.POST.getlist("numbers[]")
        codes = request.POST.getlist("codes[]")

        try:
            create_contact(name=name, numbers=numbers, codes=codes)
        except ValueError as e:
            return render(request, "contacts/add_contact.html", {"error": str(e)})

        return redirect("contacts:contact_list")
    else:
        country_codes = list_country_codes()
        return render(request, "contacts/add_contact.html", {"country_codes": country_codes})


def contact_list(request):
    contacts = list_contacts()
    return render(request, "contacts/contact_list.html", {"contacts": contacts})


def contact_detail(request, pk):
    try:
        contact = get_contact(pk=pk)
    except Http404:
        return render(request, "404.html", status=404)
    return render(request, "contacts/contact_detail.html", {"contact": contact})


def delete_contact(request, pk):
    contact = get_contact(pk=pk)
    contact.delete()
    return redirect("contacts:contact_list")


def edit_contact(request, pk):
    contact = get_contact(pk=pk)
    if request.method == "POST":
        id = request.POST["contact_id"]
        name = request.POST["name"]
        numbers = request.POST.getlist("numbers[]")
        codes = request.POST.getlist("codes[]")
        update_contact(id=id, name=name, numbers=numbers, codes=codes)
        return redirect("contacts:contact_list")
    else:
        country_codes = list_country_codes
        return render(request, "contacts/edit_contact.html", {"contact": contact, "country_codes": country_codes})


def delete_phone(request, pk):
    contact = delete_phone_number(pk=pk)
    return redirect("contacts:contact_detail", pk=contact.pk)
