from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_login(login):
    if User.objects.filter(username=login):
        raise ValidationError('Podany użytkownik już istnieje!')
