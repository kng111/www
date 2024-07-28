from django.core.exceptions import ValidationError
import string


def validate_password(password1, password2):
    """
    Валидатор пароля, который проверяет,
    содержит ли пароль как минимум одну
    заглавную букву, одну строчную букву,
    одну цифру и один символ.
    """
    # Проверка длины пароля
    if len(password1) < 8:
        return False

    # Проверка наличия заглавных букв
    if not any(char.isupper() for char in password1):
        return False

    # Проверка наличия строчных букв
    if not any(char.islower() for char in password1):
        return False

    # Проверка наличия цифр
    if not any(char.isdigit() for char in password1):
        return False

    # Проверка наличия символов
    if not any(char in string.punctuation for char in password1):
        return False

    # Пароли совпадают или нет
    if password1 != password2:
        return False

    # Если все проверки пройдены, возвращаем True
    return True
