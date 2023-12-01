from django.contrib import admin

from .models import (
    Book, 
    Author,
    Review,
)

class ReviewInline(admin.TabularInline):
    model = Review

class BookInline(admin.TabularInline):
    model = Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [
        ReviewInline,
    ]
    list_display = ["title", "author", "price"]

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [
        BookInline,
    ]
    list_display = ["first_name", "last_name", "born"]