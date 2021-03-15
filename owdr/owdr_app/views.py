from django.http import HttpResponse
from django.views import View
from .models import Donation, Institution, InstitutionCategory, Category, DonationCategory
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import CreateUserForm, LoginForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def listing(request, objects_list, page):
    paginator = Paginator(objects_list, 5)
    page_name = request.GET.get(page)
    return paginator.get_page(page_name)


def InstitutionCategoryToString(institution):
    categories = InstitutionCategory.objects.filter(institution=institution)
    categoryList = []
    for category in categories:
        categoryList.append(category.category.name)
    str1 = ", "
    return str1.join(categoryList)


class LandingPage(View):

    def get(self, request):
        donations = Donation.objects.all()
        donated_quantity = 0
        donated_organisations = []
        for donation in donations:
            donated_quantity += donation.quantity
            donated_organisations.append(donation.institution)
        donated_organisations = len(set(donated_organisations))

        foundations = Institution.objects.filter(type=1)
        for foundation in foundations:
            foundation.category = InstitutionCategoryToString(foundation)
        foundations = listing(request, foundations, 'fundations')
        organisations = Institution.objects.filter(type=2)
        for organisation in organisations:
            organisation.category = InstitutionCategoryToString(organisation)
        organisations = listing(request, organisations, 'organisations')
        gatherings = Institution.objects.filter(type=3)
        for gathering in gatherings:
            gathering.category = InstitutionCategoryToString(gathering)
        gatherings = listing(request, gatherings, 'gathering')
        return render(request, 'index.html',
                      {"donated_quantity": donated_quantity, "donated_organisations": donated_organisations,
                       "foundations": foundations, "organisations": organisations, "gatherings": gatherings})


class Login(View):

    def get(self, request):

        form = LoginForm
        return render(request, 'login.html', {'form': form})

    def post(self, request):

        rec_form = LoginForm(request.POST)
        if rec_form.is_valid():
            user_name = rec_form.cleaned_data['login']
            password = rec_form.cleaned_data['password']
            user = authenticate(username=user_name, password=password)
            if user:
                login(request, user)
                return redirect('/#')
            else:
                return redirect('/register/#register')


class Logout(View):
    """Logging out current user."""

    def get(self, request):
        logout(request)
        return redirect('/')


class Register(View):

    def get(self, request):
        form = CreateUserForm
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            User.objects.create_user(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect('/login/#login')


class AddDonation(View):

    def get(self, request):

        if request.user.is_authenticated:
            categories = Category.objects.all()
            institutions = Institution.objects.all()
            return render(request, 'form.html', {"categories": categories, "institutions": institutions})
        else:
            return redirect('/login/#login')


def DonationCategoryToString(donation):
    categories = DonationCategory.objects.filter(donation=donation)
    categoryList = []
    for category in categories:
        categoryList.append(category.category.name)
    str1 = ", "
    return str1.join(categoryList)


class UserView(View):

    def get(self, request):
        donations = Donation.objects.filter(user=request.user)
        for donation in donations:
            donation.category = DonationCategoryToString(donation)
        return render(request, 'user.html', {"donations": donations})
