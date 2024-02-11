from django.urls import path

from phonebook.contacts.views import (
    AddContactView,
    ContactDetailView,
    ContactListView,
    DeleteContactView,
    DeletePhoneView,
)

app_name = "contacts"

urlpatterns = [
    path("add/", AddContactView.as_view(), name="add_contact"),
    path("", ContactListView.as_view(), name="contact_list"),
    path("<int:pk>/", ContactDetailView.as_view(), name="contact_detail"),
    path("<int:pk>/delete/", DeleteContactView.as_view(), name="delete_contact"),
    path("phone_number/<int:pk>/delete/", DeletePhoneView.as_view(), name="delete_phone_number"),
]
