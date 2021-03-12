from django.contrib import admin
from .models import Donation, Category, Institution, InstitutionCategory, DonationCategory
# Register your models here.

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(InstitutionCategory)
admin.site.register(DonationCategory)
