from django.urls import path

from .views import (
    AuthorListView,
    AuthorDetailView,
    BookListView, 
    BookDetailView
)

urlpatterns = [
    path("authors/<uuid:pk>", AuthorDetailView.as_view(), name="author_detail"),
    path("authors/", AuthorListView.as_view(), name="author_list"),
    path("books/<uuid:pk>", BookDetailView.as_view(), name="book_detail"),
    path("books/", BookListView.as_view(), name="book_list"),
]