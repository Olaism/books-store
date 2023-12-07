from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
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
        subs = Subscription.objects.filter(user=self.request.user, verified=True)
        try:
            user_sub = subs[0]
            user_sub_type = user_sub.subscription_plan.sub_type
        except IndexError:
            user_sub_type = None
        context["user_sub_type"] = user_sub_type
        return context

class BookDetailView(
    LoginRequiredMixin, 
    UserPassesTestMixin,
    generic.DetailView):
    model = Book
    template_name = "books/detail.html"
    context_object_name = "book" 
    
    def test_func(self):
        pk = self.kwargs.get('pk')   # get the pk
        book = Book.objects.get(pk=pk) # get the book instance
        user = self.request.user #get the login user
        subs = Subscription.objects.filter(user=user, verified=True)
        if len(subs) == 0:
            return book.plan_type == "FR"
        sub_type = subs[0].subscription_plan.sub_type
        if sub_type == "BS":
            return book.plan_type == "FR" or book.plan_type == "BS"
        return sub_type == "PR"

