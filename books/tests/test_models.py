import uuid
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from ..models import (
    Author,
    Book,
    Review
)

class AuthorModelDefaultTests(TestCase):

    def setUp(self):
        self.author = Author(
            first_name="test",
            last_name="user",
        )

    def test_author_listing(self):
        self.assertTrue(type(self.author.id) == uuid.UUID)
        self.assertTrue(self.author.id.version, 4)
        self.assertEqual(self.author.first_name, "test")
        self.assertEqual(self.author.last_name, "user")
        self.assertIsNone(self.author.born)
        self.assertEqual(self.author.get_name, "user test")

    def test_absolute_url(self):
        self.assertEqual(
            self.author.get_absolute_url(), 
            f"/authors/{self.author.id}")

class AuthorModelTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name="lens",
            last_name="arsenal",
            born=timezone.datetime(1980, 1, 1)
        )

    def test_author_listing(self):
        self.assertTrue(type(self.author.id) == uuid.UUID)
        self.assertTrue(self.author.id.version, 4)
        self.assertEqual(self.author.first_name, "lens")
        self.assertEqual(self.author.last_name, "arsenal")
        self.assertEqual(self.author.born, timezone.datetime(1980, 1, 1))
        self.assertEqual(self.author.get_name, "arsenal lens")

    def test_absolute_url(self):
        self.assertEqual(
            self.author.get_absolute_url(), 
            f"/authors/{self.author.id}")


class BookModelDefaultTests(TestCase):

    def setUp(self):
        self.author = Author.objects.create(
            first_name="Antonio", 
            last_name="Mele"
        )
        self.book = Book(
            title="Django by example",
            author=self.author,
            price=10.99
        )

    def test_book_listing(self):
        self.assertEqual(self.book.title, "Django by example")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.price, 10.99)
        self.assertEqual(self.book.plan_type, "FR")
        self.assertIsNotNone(self.book.cover)

    def test_absolute_url(self):
        self.assertEqual(self.book.get_absolute_url(), f"/books/{self.book.id}")


class BookModelTests(TestCase):

    def setUp(self):
        self.book_cover = SimpleUploadedFile(
            "sample.png", 
            b"sample content", 
            content_type="image/png"
        )
        self.sample_doc = SimpleUploadedFile("sample.pdf", b"doc content")
        self.author = Author.objects.create(
            first_name="Antonio", 
            last_name="Mele"
        )
        self.book = Book(
            title="Django by example",
            author=self.author,
            price=10.99,
            cover=self.book_cover,
            plan_type="PR",
            doc=self.sample_doc,
        )

    def test_book_listing(self):
        self.assertEqual(self.book.title, "Django by example")
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.book.price, 10.99)
        self.assertEqual(self.book.cover, self.book_cover)
        self.assertEqual(self.book.plan_type, "PR")
        self.assertEqual(self.book.doc, self.sample_doc)

    def test_absolute_url(self):
        self.assertEqual(self.book.get_absolute_url(), f"/books/{self.book.id}")


class ReviewModelTest(BookModelTests):

    def setUp(self):
        super().setUp()
        self.user = get_user_model().objects.create_user(
            username="papa",
            email="papa@mail.com",
            password="papapassword"
        )
        self.review = Review(
            book=self.book,
            review="An excellent review.",
            author=self.user
        )
        
    def test_review_listing(self):
        self.assertEqual(self.review.review, "An excellent review.")
        self.assertEqual(self.review.author, self.user)
        self.assertEqual(self.review.book, self.book)
