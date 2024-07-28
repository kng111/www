from django.contrib.auth.models import AbstractUser
from django.db import models
from roles.models import MyGroup, Role  # Импортируем модель Role


class User(AbstractUser):
    """Собственная модель пользователя"""

    GENDER_CHOICES = (
        ('М', 'Мужской'),
        ('Ж', 'Женский'),
    )

    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, null=True, blank=True
    )
    phone_number = models.CharField(max_length=11)
    role = models.ForeignKey(
        Role,  # Используем модель Role здесь
        on_delete=models.SET_NULL,
        null=True,
    )
    groups = models.ManyToManyField(MyGroup, blank=True, related_name='users')

    def __str__(self):
        return f'{self.username} - {self.role}'
