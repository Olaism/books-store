from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Author, Book
from ..views import (
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView
)

User = get_user_model()

class BaseSetUp(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name="ty",
            last_name="hy"
        )
        self.book = Book.objects.create(
            title="The journey of hy-ty",
            author=self.author,
            price=40.99
        )

class UserBaseSetUp(BaseSetUp):

    def setUp(self):
        super().setUp()
        # create a user
        self.email = "testuser@example.com"
        self.password = "testpassword"
        self.user = User.objects.create_user(
            username="testuser",
            email=self.email,
            password=self.password
        )
        self.client.login(email=self.email, password=self.password)

class LoginRequiredAuthorListViewTest(BaseSetUp):

    def test_redirection(self):
        url = reverse('author_list')
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, 
            f'{login_url}?next={url}')

class LoginRequiredAuthorDetailViewTest(BaseSetUp):

    def test_redirection(self):
        url = self.author.get_absolute_url()
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={url}')

class LoginRequiredBookListViewTest(BaseSetUp):

    def test_redirection(self):
        url = reverse('book_list')
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={url}')

class LoginRequiredBookDetailViewTest(BaseSetUp):

    def test_redirection(self):
        url = self.book.get_absolute_url()
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={url}')

class PermissionRequiredBookDetailViewTest(UserBaseSetUp):

    def test_permission_required(self):
        response = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response.status_code, 403)


class AuthorListViewTest(UserBaseSetUp):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('author_list'))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve("/authors/")
        self.assertEqual(view.func.__name__, AuthorListView.as_view().__name__)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "authors/list.html")
        self.assertTemplateUsed(self.response, "_base.html")


class AuthorDetailViewTest(UserBaseSetUp):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.author.get_absolute_url())

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve("/authors/{id}".format(id=self.author.id))
        self.assertEqual(view.func.__name__, AuthorDetailView.as_view().__name__)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "authors/detail.html")
        self.assertTemplateUsed(self.response, "_base.html")

class BookListViewTest(UserBaseSetUp):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(reverse('book_list'))

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve("/books/")
        self.assertEqual(view.func.__name__, BookListView.as_view().__name__)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "books/list.html")
        self.assertTemplateUsed(self.response, "_base.html")


class BookDetailViewTest(UserBaseSetUp):

    def setUp(self):
        super().setUp()
        perm = Permission.objects.get(codename="special_status")
        self.user.user_permissions.add(perm)
        self.response = self.client.get(self.book.get_absolute_url())

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve("/books/{id}".format(id=self.book.id))
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "books/detail.html")
        self.assertTemplateUsed(self.response, "_base.html")