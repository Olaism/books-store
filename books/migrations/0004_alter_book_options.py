# Generated by Django 4.2.7 on 2023-12-01 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_cover'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'permissions': (('special_status', 'can read all books'),)},
        ),
    ]