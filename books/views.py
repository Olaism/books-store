from django.views import generic

from .models import (
    Author,
    Book
)

class AuthorListView(generic.ListView):
    model = Author
    template_name = "authors/list.html"
    context_object_name = "author_list"

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = "authors/detail.html"
    context_object_name = "author"

class BookListView(generic.ListView):
    model = Book
    template_name = "books/list.html"
    context_object_name = "book_list"

class BookDetailView(generic.DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"