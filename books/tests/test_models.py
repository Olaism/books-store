from django.test import TestCase
from django.utils import timezone

from ..models import (
    Author,
    Book
)

class AuthorModelTests(TestCase):

    def setUp(self):
        self.author1 = Author(
            first_name="test",
            last_name="user",
        )
        self.author2 = Author.objects.create(
            first_name="lens",
            last_name="arsenal",
            born=timezone.datetime(1980, 1, 1)
        )

    def test_author1_listing(self):
        self.assertEqual(self.author1.first_name, "test")
        self.assertEqual(self.author1.last_name, "user")
        self.assertEqual(self.author1.born, None)

    def test_author2_listing(self):
        self.assertEqual(self.author2.first_name, "lens")
        self.assertEqual(self.author2.last_name, "arsenal")
        self.assertEqual(self.author2.born, timezone.datetime(1980, 1, 1))

    def test_absolute_url(self):
        self.assertEqual(self.author2.get_absolute_url(), f"/authors/{self.author2.id}")


class BookModelTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(first_name="ty", last_name="hy")
        self.book = Book(
            title="Hello world",
            author=self.author,
            price=10.99
        )

    def test_book_listing(self):
        self.assertEqual(self.book.title, "Hello world")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.price, 10.99)

    def test_absolute_url(self):
        self.assertEqual(self.book.get_absolute_url(), f"/books/{self.book.id}")