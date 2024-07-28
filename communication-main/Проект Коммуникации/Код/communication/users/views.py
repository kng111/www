from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.views import View
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.contrib.auth.forms import SetPasswordForm
from django.db.utils import IntegrityError
from django.db import IntegrityError
from django.contrib.auth.models import Group
from users.models import User
from .models import MyGroup
from django.core.exceptions import ValidationError
from .utils import validate_password
from .models import Role

from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.views.generic import TemplateView


class ProfileView(TemplateView):

    template_name = "users/profile.html"

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("login")
        return super().get(request)


class HomeView(TemplateView):
    template_name = 'users/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['is_in_sb_group'] = user.groups.filter(name="СБ").exists()
        context['is_in_prodazhi_group'] = user.groups.filter(name="Продажи").exists()
        context['is_in_sis_admin'] = user.groups.filter(name="Сис админ").exists()
        return context
    
class CreateUserView(View):

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, "users/create_user.html", {"form": form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                error_message = "Такая почта уже зарегистрирована. Пожалуйста, используйте другую почту."
                return render(
                    request,
                    "users/create_user.html",
                    {"form": form, "error_message": error_message},
                )

            if not validate_password(
                form.cleaned_data.get("password1"),
                form.cleaned_data.get("password2"),
            ):
                error_message = """Пароль должен содержать не менее 8 символов,
                                одну заглавную букву, одну строчную букву, одну цифру и один символ."""
                return render(
                    request,
                    "users/create_user.html",
                    {"form": form, "error_message": error_message},
                )
            form.save()
            return render(
                request,
                "users/home.html",
            )
        else:
            error_message = "Пожалуйста, заполните форму корректно."
            context = {"form": form, "error_message": error_message}
            return render(request, "users/create_user.html", context)


class LoginView(View):

    def get(self, request):
        return render(request, "users/login.html")

    def post(self, request):
        login_field = request.POST.get("username")
        password = request.POST.get("password")

        # Проверяем, есть ли пользователь с указанным логином или email
        user = User.objects.filter(
            Q(username=login_field) | Q(email=login_field)
        ).first()
        if user is not None:
            # Если пользователь найден, проверяем его пароль
            if user.check_password(password):
                login(request, user)
                return redirect("home")
            else:
                return render(
                    request,
                    "users/login.html",
                    {"error": "Неверный пароль."},
                )
        else:
            return render(
                request,
                "users/login.html",
                {"error": "Пользователь с таким логином или email не найден."},
            )


class LogoutView(View):

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return redirect("/")


class CustomPasswordResetView(PasswordResetView):
    template_name = "registration/password_reset_form.html"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "registration/password_reset_confirm.html"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "registration/password_reset_complete.html"


class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "registration/change_password.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Вы успешно сменили пароль!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибку ниже.")
        return super().form_invalid(form)


class GetUserByEmailView(View):

    def get(self, request, *args, **kwargs):
        email = kwargs.get("email")
        try:
            user = User.objects.get(email=email)
            return HttpResponse(f"Найден пользователь: {user.username}")
        except User.DoesNotExist:
            return HttpResponse(
                f'Пользователь с адресом электронной почты "{email}" не найден'
            )


class TableView(UserPassesTestMixin, TemplateView):
    template_name = 'users/show_table.html'

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name="Сис админ").exists() or user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['users'] = User.objects.all()
        context['groups'] = Group.objects.all()
        context['is_in_sis_admin'] = user.groups.filter(name="Сис админ").exists()
        return context


class ChangeUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                users = User.objects.exclude(is_superuser=True)
                roles = Role.objects.all()
                groups = MyGroup.objects.all()
            elif request.user.role and request.user.role.name == "Главный админ":
                users = User.objects.filter(
                    role__name__in=["Сотрудник", "Менеджер"],
                    is_superuser=False,
                )
                roles = Role.objects.filter(name__in=["Сотрудник", "Менеджер"])
                groups = MyGroup.objects.all()
            elif request.user.role and request.user.role.name == "Менеджер":
                users = User.objects.filter(role__name="Сотрудник")
                roles = Role.objects.filter(name="Сотрудник")
                groups = MyGroup.objects.all()
            else:
                users = User.objects.none()
                roles = Role.objects.none()
                groups = MyGroup.objects.none()
        else:
            users = User.objects.none()
            roles = Role.objects.none()
            groups = MyGroup.objects.none()

        return render(
            request,
            "users/change_user.html",
            {"users": users, "roles": roles, "groups": groups},
        )

    def post(self, request):
        user_id = request.POST.get("user")
        group_ids = request.POST.getlist("groups")
        user = User.objects.get(id=user_id)

        if request.user.is_superuser:
            role_id = request.POST.get("role")
            user.role = Role.objects.get(id=role_id)

        user.groups.set(MyGroup.objects.filter(id__in=group_ids))
        user.save()

        return redirect("home")

class GetUserDataView(View):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        user_data = {
            "role": user.role.id if user.role else None,
            "groups": list(user.groups.values_list('id', flat=True)),
        }
        return JsonResponse(user_data)