from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from roles.models import Role
from users.forms import CustomUserCreationForm

User = get_user_model()


class CreateUserViewTest(TestCase):
    def test_post_request_valid_data(self):
        # Create a role for the user
        role = Role.objects.create(name='Сотрудник')

        # Create form data
        form_data = {
            'email': 'test@example.com',
            'first_name': 'Егор',
            'last_name': 'Бойко',
            'password1': 'Testpassword123.',
            'password2': 'Testpassword123.',
            'birth_date': '2000-01-01',
            'gender': 'М',
            'phone_number': '1234567890',
            'role': role.id,
        }

        # Create the form instance with the updated form data
        form = CustomUserCreationForm(data=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())

        # Submit the form data to the view
        response = self.client.post(reverse('create_user'), form_data)

        # Check if the user object was created in the database
        self.assertTrue(User.objects.filter(email='test@example.com').exists())

        # Check if the response status code is 200 (indicating successful form submission)
        self.assertEqual(response.status_code, 200)

    def test_post_request_invalid_data(self):
        form_data = {}  # Invalid form data
        response = self.client.post(reverse('create_user'), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/create_user.html')
        self.assertFalse(
            User.objects.filter(email='test@example.com').exists()
        )


class LoginViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123'
        )

    def test_get_request(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_post_request_valid_credentials(self):
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

    def test_post_request_invalid_credentials(self):
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertIn(
            'Неверное имя пользователя или пароль.', response.content.decode()
        )


class LogoutViewTest(TestCase):
    def test_logout(self):
        user = User.objects.create_user(
            username='testuser', password='testpassword123'
        )
        self.client.force_login(user)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class ChangeUserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword123'
        )

    def test_get_request_superuser(self):
        # Create a superuser
        user = User.objects.create_superuser(
            username='superuser',
            email='superuser@example.com',
            password='testpassword123',
        )
        self.client.force_login(user)

        # Make a GET request to the view
        response = self.client.get(reverse('change_user'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_user.html')

    def test_get_request_non_superuser(self):
        # Authenticate a regular user
        self.client.force_login(self.user)

        # Make a GET request to the view
        response = self.client.get(reverse('change_user'))

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/change_user.html')
