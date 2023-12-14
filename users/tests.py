from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.test import TestCase
from django.urls import reverse, resolve

from allauth.account.views import SignupView
from allauth.account.forms import SignupForm

from .views import ProfileView

User = get_user_model()

class CustomUserTest(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            username='testuser',
            email='testuser@mail.com',
            password='testpassword'
        )

        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@mail.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            username="superuser",
            email="superuser@mail.com",
            password="superpassword"
        )

        self.assertEqual(user.username, "superuser")
        self.assertEqual(user.email, "superuser@mail.com")
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

class SignUpPageTest(TestCase):

    def setUp(self):
        url = reverse('account_signup')
        self.response = self.client.get(url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_templates_used(self):
        self.assertTemplateUsed(self.response, "account/signup.html")
        self.assertTemplateUsed(self.response, "_base.html")

    def test_resolve_correct_view(self):
        view = resolve("/accounts/signup/")
        self.assertEqual(view.func.__name__, SignupView.as_view().__name__)

    def test_form_instance(self):
        form = self.response.context.get("form")
        self.assertIsInstance(form, SignupForm)

    def test_contains_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_html(self):
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="password', 2)

class LoginRequiredProfilePageTest(TestCase):

    def test_redirection(self):
        url = reverse('user_profile')
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertRedirects(response, f"{login_url}?next={url}")

class ProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="ty", 
                    email="ty01@mail.com", password="typassword123")
        self.client.login(email="ty01@mail.com", password="typassword123")
        self.url = reverse("user_profile")

class ProfilePageTest(ProfileTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.url)

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_correct_url(self):
        view = resolve("/profile/")
        self.assertEqual(view.func.view_class, ProfileView)

    def test_form_instance(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)
    
    def test_contain_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_form_inputs(self):
        self.assertContains(self.response, 'type="text"', 3)

    def test_no_profile_photo_display(self):
        self.assertContains(self.response, '/static/img/user_avatar.png')

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "users/profile.html")
        self.assertTemplateUsed(self.response, "_base.html")

class ProfilePagePostTest(ProfileTestCase):

    def setUp(self):
        super().setUp()
        self.new_username = 'francis01'
        self.first_name = 'francis'
        self.last_name = 'ollburg'
        self.response = self.client.post(self.url, {
            'username': self.new_username,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('user_profile'))

    def test_user_update(self):
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, self.new_username)
        self.assertEqual(self.user.first_name, self.first_name)
        self.assertEqual(self.user.last_name, self.last_name)

class ProfilePageInvalidPostTest(ProfileTestCase):

    def setUp(self):
        super().setUp()
        self.response = self.client.post(self.url, {})

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)