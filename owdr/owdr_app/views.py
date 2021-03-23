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

    def post(self, request):
        quantity = request.POST['bags']
        institution = Institution.objects.get(pk=request.POST['organization'])
        address = request.POST['address']
        city = request.POST['city']
        zip_code = request.POST['postcode']
        phone_number = request.POST['phone']
        pick_up_date = request.POST['data']
        pick_up_time = request.POST['time']
        pick_up_comment = request.POST.get('more_info')
        user = request.user
        object = Donation.objects.create(
            quantity=quantity, institution=institution, address=address,
            phone_number=phone_number, city=city, zip_code=zip_code, pick_up_date=pick_up_date,
            pick_up_time=pick_up_time, pick_up_comment=pick_up_comment, user=user
        )
        object.save()
        categories = request.POST.getlist('categories')
        print(categories)
        for category in categories:
            print(category)
            cat = Category.objects.get(pk=category)
            object.categories.add(cat)
        return render(request, 'form-confirmation.html')


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


class IsTaken(View):

    def get(self, request, pk):
        donation = Donation.objects.get(pk=pk)
        if donation.is_taken:
            donation.is_taken = False
        else:
            donation.is_taken = True
        donation.save()
        return redirect('/user/')


class EditUser(View):

    def get(self, request):
        return render(request, 'user-edit.html')

    def post(self, request):
        user = request.user
        if request.POST.get('password'):
            password = request.POST.get('password')
            authentication = authenticate(username=user.username, password=password)
            if authentication:
                if request.POST.get('name'):
                    name = request.POST.get('name')
                    user.first_name = name
                if request.POST.get('surname'):
                    surname = request.POST.get('surname')
                    user.last_name = surname
                if request.POST.get('email'):
                    email = request.POST.get('email')
                    user.email = email
                user.save()
                return redirect('/user/')
            else:
                pop = "Niepoprawne hasło"
                return render(request, 'user-edit.html', {'pop': pop})
        else:
            password2 = request.POST.get('password2')
            authentication2 = authenticate(username=user.username, password=password2)
            if authentication2:
                if request.POST.get('new-password') == request.POST.get('new-password2'):
                    user.password = request.POST.get('new-password')
                    return redirect('/user/')
                else:
                    pop2 = "Niepoprawne hasło"
                    return render(request, 'user-edit.html', {'pop2': pop2})
