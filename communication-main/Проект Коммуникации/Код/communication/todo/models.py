from django.db import models
from roles.models import MyGroup # Импортируем модель MyGroup
from users.models import User # Импортируем модель User


class ToDo(models.Model):

    PRIORITY_DATA = (
        ('high', 'Высокий приоритет'),
        ('medium', 'Средний приоритет'),
        ('low', 'Низкий приоритет')
    )

    task = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    employee = models.ForeignKey(
        User,  # Используем модель User здесь
        on_delete=models.SET_NULL,
        null=True,
    )
    group = models.ForeignKey(
        MyGroup,  # Используем модель MyGroup здесь
        on_delete=models.SET_NULL,
        null=True,
    )
    priority = models.CharField(max_length=20, choices=PRIORITY_DATA, null=True)
    date = models.DateField(null=True)
    is_complete = models.BooleanField(null=True, blank = True, default = False)

    def __str__(self):
        return self.task

