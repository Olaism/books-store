from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views import generic

from .models import (
    Author,
    Book
)

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    template_name = "authors/list.html"
    context_object_name = "author_list"

class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    template_name = "authors/detail.html"
    context_object_name = "author"

class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    template_name = "books/list.html"
    context_object_name = "book_list"

class BookDetailView(
    LoginRequiredMixin, 
    PermissionRequiredMixin,
    generic.DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"
    permission_required = "books.special_status"