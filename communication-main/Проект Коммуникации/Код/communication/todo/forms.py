from django import forms
from .models import ToDo

class Todo_form(forms.ModelForm):
    class Meta:
        model = ToDo
        fields = ['task', 'description', 'group', 'employee', 'priority', 'date']
        labels = {
            'task': 'Задача',
            'description': 'Описание',
            'group': 'Отдел',
            'employee': 'Сотрудник',
            'priority': 'Приоритет',
            'date': 'Дата выполнения'
            }
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}, format=('%Y-%m-%d'))
        }
