from django.contrib import admin
from .models import ToDo
# Register your models here.

@admin.register(ToDo)
class NotesDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'task', 'description', 'employee', 'priority', 'date', 'group']
    # list_editable = ['content']
    ordering = ['id']
    list_per_page = 5

