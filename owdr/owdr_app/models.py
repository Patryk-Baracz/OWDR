from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Nazwa")


class Institution(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Nazwa")
    description = models.TextField(verbose_name="Opis")
    TYPES = [
        (1, "Fundacja"),
        (2, "Organizacja pozarządowa"),
        (3, "Zbiórka lokalna"),
    ]
    type = models.IntegerField(choices=TYPES, default=1, verbose_name="Typ")
    categories = models.ManyToManyField(Category, through="InstitutionCategory", verbose_name="Kategoria")


class InstitutionCategory(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Donation(models.Model):
    quantity = models.IntegerField(verbose_name="Liczba worków")
    categories = models.ManyToManyField(Category, through="DonationCategory", verbose_name="Kategoria")
    institution = models.ForeignKey(Institution, verbose_name="Instytucja")
    address = models.CharField(max_length=120, verbose_name="Ulica i numer domu")
    phone_number = models.CharField(max_length=12, verbose_name="Numer telefonu")
    city = models.CharField(max_length=34, verbose_name="Miasto")
    zip_code = models.CharField(max_length=6, verbose_name="Kod pocztowy")
    pick_up_date = models.DateField(verbose_name="Data odbioru")
    pick_up_time = models.TimeField(verbose_name="Godzina odbioru")
    pick_up_comment = models.TextField(verbose_name="Komentarz")
    user = models.ForeignKey(User, Null=True, on_delete=models.CASCADE)


class DonationCategory(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
