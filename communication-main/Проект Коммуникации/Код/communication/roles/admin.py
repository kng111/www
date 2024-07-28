from django.contrib import admin
from django.contrib.auth.models import Group
from .models import MyGroup, Role


@admin.register(MyGroup)
class MyGroupAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.unregister(Group)  # Отменяем регистрацию стандартной модели Group
