import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class Book(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    title = models.CharField(max_length=255)
    author = models.ForeignKey("Author", related_name="books", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', args=(self.id,))

class Author(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    born = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.last_name.upper()}, {self.first_name}"

    def get_absolute_url(self):
        return reverse('author_detail', args=(self.id,))

    @property
    def get_name(self):
        return self.last_name + " " + self.first_name

class Review(models.Model):
    book = models.ForeignKey(Book, related_name='reviews', on_delete=models.CASCADE)
    review = models.CharField(max_length=255)
    author = models.ForeignKey(
        get_user_model(),
        related_name='reviews',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.review