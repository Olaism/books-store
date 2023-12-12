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
from subscription.models import (
    Subscription,
    SubscriptionPlan
)

User = get_user_model()

class BaseSetUp(TestCase):

    def setUp(self):
        # create an author
        self.author = Author.objects.create(
            first_name="William",
            last_name="Vincent"
        )
        # create three categories of books
        self.free_book = Book.objects.create(
            title="Django For Beginners",
            author=self.author,
            price=29.99
        )
        self.basic_book = Book.objects.create(
            title="Django For Professionals",
            author=self.author,
            price=39.99,
            plan_type="BS"
        )
        self.premium_book = Book.objects.create(
            title="Django For APIs",
            author=self.author,
            price=49.99,
            plan_type="PR"
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

class FreeUserBaseSetUp(UserBaseSetUp):

    def setUp(self):
        super().setUp()
        self.client.login(email=self.email, password=self.password)

class BasicUserBaseSetUp(UserBaseSetUp):

    def setUp(self):
        super().setUp()
        plan = SubscriptionPlan.objects.create(
            sub_type="BS",
            name = "sub plan for basic user",
            price = 1000.00,
        )
        Subscription.objects.create(
            subscription_plan=plan,
            user=self.user,
            verified=True
        )
        self.client.login(email=self.email, password=self.password)

class PremiumUserBaseSetUp(UserBaseSetUp):

    def setUp(self):
        super().setUp()
        plan = SubscriptionPlan.objects.create(
            sub_type="PR",
            name = "sub plan for premium user",
            price = 3000.00,
        )
        Subscription.objects.create(
            subscription_plan=plan,
            user=self.user,
            verified=True
        )
        self.client.login(email=self.email, password=self.password)

class LoginRequiredBookListViewTest(BaseSetUp):

    def test_redirection(self):
        url = reverse('book_list')
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={url}')

class LoginRequiredBookDetailViewTest(BaseSetUp):

    def test_redirection_for_free_book(self):
        url = self.free_book.get_absolute_url()
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_redirection_for_basic_book(self):
        url = self.basic_book.get_absolute_url()
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={url}')

    def test_redirection_for_premium_book(self):
        url = self.premium_book.get_absolute_url()
        login_url = reverse('account_login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'{login_url}?next={url}')

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

class AuthorListViewTest(FreeUserBaseSetUp):

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


class AuthorDetailViewTest(FreeUserBaseSetUp):

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

class BookListViewTest(FreeUserBaseSetUp):

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


class BookDetailViewForFreeUserTest(FreeUserBaseSetUp):

    def setUp(self):
        super().setUp()
        # default response is for free_book
        self.response = self.client.get(self.free_book.get_absolute_url())

    def test_free_book_status_code_for_not_subscribed_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_basic_book_status_code_for_not_subscribed_user(self):
        response = self.client.get(self.basic_book.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_premium_book_status_code_for_not_subscribed_user(self):
        response = self.client.get(self.premium_book.get_absolute_url())
        self.assertEqual(response.status_code, 403)

    def test_resolve_url_for_free_book_detail_view(self):
        view = resolve("/books/{id}".format(id=self.free_book.id))
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)

    def test_template_used_for_free_book_detail_view(self):
        self.assertTemplateUsed(self.response, "books/detail.html")
        self.assertTemplateUsed(self.response, "_base.html")

class BookDetailViewForBasicUserTest(BasicUserBaseSetUp):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.basic_book.get_absolute_url())

    def test_free_book_status_code_for_basic_subscription_user(self):
        response = self.client.get(
            self.free_book.get_absolute_url()
        )
        self.assertEqual(response.status_code, 200)

    def test_basic_book_status_code_for_basic_subscription_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_premium_book_status_code_for_basic_subscription_user(self):
        response = self.client.get(
            self.premium_book.get_absolute_url()
        )
        self.assertEqual(response.status_code, 403)

    def test_resolve_url_for_basic_book_detail_view(self):
        view = resolve("/books/{id}".format(id=self.basic_book.id))
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)
    
    def test_template_used_for_basic_book_detail_view(self):
        self.assertTemplateUsed(self.response, "books/detail.html")
        self.assertTemplateUsed(self.response, "_base.html")

class BookDetailViewForPremiumUserTest(PremiumUserBaseSetUp):

    def setUp(self):
        super().setUp()
        self.response = self.client.get(self.premium_book.get_absolute_url())

    def test_free_book_status_code_for_premium_subscription_user(self):
        response = self.client.get(self.free_book.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_basic_book_status_code_for_premium_subscription_user(self):
        response = self.client.get(self.basic_book.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_premium_book_status_code_for_premium_subscription_user(self):
        self.assertEqual(self.response.status_code, 200)

    def test_resolve_url_for_premium_book_detail_view(self):
        view = resolve("/books/{id}".format(id=self.premium_book.id))
        self.assertEqual(view.func.__name__, BookDetailView.as_view().__name__)
    
    def test_template_used_for_premium_book_detail_view(self):
        self.assertTemplateUsed(self.response, "books/detail.html")
        self.assertTemplateUsed(self.response, "_base.html")