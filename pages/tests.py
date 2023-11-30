from django.test import SimpleTestCase
from django.urls import resolve, reverse

from .views import HomePageView, AboutPageView

class HomePageViewTests(SimpleTestCase):

    def setUp(self):
        self.response = self.client.get(reverse('home'))

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_resolves_correct_url(self):
        view = resolve('/')
        self.assertEqual(view.func.view_class, HomePageView)
        self.assertEqual(view.url_name, 'home')

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'pages/home.html')
        self.assertTemplateUsed(self.response, '_base.html')

class AboutPageViewTests(SimpleTestCase):

    def setUp(self):
        self.response = self.client.get(reverse('about'))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_view_resolves_correct_url(self):
        view = resolve("/about/")
        self.assertEqual(view.func.__name__, AboutPageView.as_view().__name__)

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "pages/about.html")
        self.assertTemplateUsed(self.response, "_base.html")