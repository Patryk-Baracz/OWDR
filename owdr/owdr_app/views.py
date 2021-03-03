from django.shortcuts import render
from django.views import View
# Create your views here.

class LandingPage(View):
    def get(self, request):
        return render(request, 'index.html')

class Login(View):
    def get(self, request):
        return render(request, 'login.html')

class Register(View):
    def get(self, request):
        return render(request, 'register.html')

class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')