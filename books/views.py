from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views import generic

from subscription.models import Subscription
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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        has_active_subscription = False # By default, the user is not subscribed
        subs = Subscription.objects.filter(user=self.request.user)
        for sub in subs:
            if sub.is_active:
                has_active_subscription = True
        context["has_active_subscription"] = has_active_subscription
        return context

class BookDetailView(
    LoginRequiredMixin, 
    PermissionRequiredMixin,
    generic.DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book"
    permission_required = "books.special_status"