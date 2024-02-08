from django.urls import path

from phonebook.contacts.views import (
    add_contact,
    contact_detail,
    contact_list,
    delete_contact,
    delete_phone,
    edit_contact,
)

app_name = "contacts"

urlpatterns = [
    path("add/", add_contact, name="add_contact"),
    path("", contact_list, name="contact_list"),
    path("<int:pk>/", contact_detail, name="contact_detail"),
    path("<int:pk>/edit/", edit_contact, name="edit_contact"),
    path("<int:pk>/delete/", delete_contact, name="delete_contact"),
    path("phone_number/<int:pk>/delete/", delete_phone, name="delete_phone_number"),
]
