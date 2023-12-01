from django.test import TestCase
from django.urls import reverse, resolve

from ..models import Author, Book
from ..views import (
    BookListView,
    BookDetailView,
    AuthorListView,
    AuthorDetailView
)

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


class AuthorListViewTest(BaseSetUp):

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


class AuthorDetailViewTest(BaseSetUp):

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

class BookListViewTest(BaseSetUp):

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


class BookDetailViewTest(BaseSetUp):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.book.get_absolute_url())

    def test_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_url(self):
        view = resolve("/books/{id}".format(id=self.book.id))
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)

    def test_template_used(self):
        self.assertTemplateUsed(self.response, "books/detail.html")
        self.assertTemplateUsed(self.response, "_base.html")