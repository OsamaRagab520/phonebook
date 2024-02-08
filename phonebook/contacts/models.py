from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CountryCode(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)


class PhoneNumber(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name="phone_numbers")
    country_code = models.ForeignKey(CountryCode, on_delete=models.CASCADE)
    number = models.CharField(max_length=20)
