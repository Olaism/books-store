# Generated by Django 4.2.7 on 2023-12-07 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_doc_book_plan_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='plan_type',
            field=models.CharField(choices=[('FR', 'FREE'), ('BS', 'BASIC'), ('PR', 'PREMIUM')], default='FR', max_length=2),
        ),
    ]