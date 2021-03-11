import django.forms as forms
from django.core.validators import EmailValidator, ValidationError
from .validators import validate_login


class CreateUserForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Imię'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Nazwisko'}))
    email = forms.CharField(validators=[EmailValidator()],
                            widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Hasło'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Powtórz hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError('Hasło nie jest takie same!')
        else:
            return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-group', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-group', 'placeholder': 'Hasło'}))
