from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="Nazwa")

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.name
    @property
    def categoriesIdString(self):
        array = []
        for el in self.categories.all():
            array.append(str(el.id))
        return ','.join(array)

class InstitutionCategory(models.Model):
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Donation(models.Model):
    quantity = models.IntegerField(null=False, verbose_name="Liczba worków")
    categories = models.ManyToManyField(Category, through="DonationCategory", verbose_name="Kategoria")
    institution = models.ForeignKey(Institution, null=False, on_delete=models.CASCADE, verbose_name="Instytucja")
    address = models.CharField(max_length=120, null=False, verbose_name="Ulica i numer domu")
    phone_number = models.CharField(max_length=12, null=False, verbose_name="Numer telefonu")
    city = models.CharField(max_length=34, null=False, verbose_name="Miasto")
    zip_code = models.CharField(max_length=6, null=False, verbose_name="Kod pocztowy")
    pick_up_date = models.DateField(null=False, verbose_name="Data odbioru")
    pick_up_time = models.TimeField(null=False, verbose_name="Godzina odbioru")
    pick_up_comment = models.TextField(verbose_name="Komentarz")
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    is_taken = models.BooleanField(verbose_name="Odebrane", null=True, default=False)


class DonationCategory(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
