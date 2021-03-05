from django.contrib import admin
from .models import Donation, Category, Institution, InstitutionCategory
# Register your models here.

admin.site.register(Donation)
admin.site.register(Category)
admin.site.register(Institution)
admin.site.register(InstitutionCategory)
