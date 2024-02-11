from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView

from phonebook.contacts.selectors import list_contacts, list_country_codes
from phonebook.contacts.services import create_contact, delete_phone_number, get_contact, update_contact


class AddContactView(View):
    def get(self, request):
        country_codes = list_country_codes()
        return render(request, "contacts/add_contact.html", {"country_codes": country_codes})

    def post(self, request):
        name = request.POST["name"]
        numbers = request.POST.getlist("numbers[]")
        codes = request.POST.getlist("codes[]")

        try:
            create_contact(name=name, numbers=numbers, codes=codes)
        except ValueError as e:
            country_codes = list_country_codes()
            return render(request, "contacts/add_contact.html", {"country_codes": country_codes, "error": str(e)})

        return redirect("contacts:contact_list")


class ContactListView(ListView):
    queryset = list_contacts()
    context_object_name = "contacts"
    paginate_by = 2
    template_name = "contacts/contact_list.html"


class ContactDetailView(View):
    def get(self, request, pk):
        try:
            contact = get_contact(pk=pk)
        except Http404:
            return render(request, "404.html", status=404)
        return render(request, "contacts/contact_detail.html", {"contact": contact})


class DeleteContactView(View):
    def get(self, request, pk):
        contact = get_contact(pk=pk)
        contact.delete()
        return redirect("contacts:contact_list")


class EditContactView(View):
    def get(self, request, pk):
        contact = get_contact(pk=pk)
        country_codes = list_country_codes()
        return render(request, "contacts/edit_contact.html", {"contact": contact, "country_codes": country_codes})

    def post(self, request, pk):
        id = request.POST["contact_id"]
        name = request.POST["name"]
        numbers = request.POST.getlist("numbers[]")
        codes = request.POST.getlist("codes[]")
        update_contact(id=id, name=name, numbers=numbers, codes=codes)
        return redirect("contacts:contact_list")


class DeletePhoneView(View):
    def get(self, request, pk):
        contact = delete_phone_number(pk=pk)
        return redirect("contacts:contact_detail", pk=contact.pk)
