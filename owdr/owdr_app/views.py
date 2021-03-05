from django.shortcuts import render
from django.views import View
from .models import Donation, Institution, InstitutionCategory
from django.core.paginator import Paginator
from django.shortcuts import render


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
        return render(request, 'login.html')


class Register(View):
    def get(self, request):
        return render(request, 'register.html')


class AddDonation(View):
    def get(self, request):
        return render(request, 'form.html')
