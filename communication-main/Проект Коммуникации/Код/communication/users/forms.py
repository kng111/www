from .models import User, MyGroup
from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.forms import AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        ),
    )
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}
        ),
    )


class CustomUserCreationForm(UserCreationForm):
    birth_date = forms.DateField(
        required=False,
        widget=forms.DateInput(
            attrs={'class': 'form-control', 'placeholder': 'Дата рождения'}
        ),
    )
    gender = forms.ChoiceField(
        choices=User.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    phone_number = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}
        ),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Имя'}
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Фамилия'}
        ),
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}
        ),
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=MyGroup.objects.all(),  # Используйте вашу модель MyGroup
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
            'birth_date',
            'gender',
            'phone_number',
            'role',
            'groups',
        )

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['email']
        if commit:
            user.save()
            self.save_m2m()
        return user
