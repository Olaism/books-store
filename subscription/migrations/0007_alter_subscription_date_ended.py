# Generated by Django 4.2.7 on 2023-12-05 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0006_alter_subscription_date_started'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='date_ended',
            field=models.DateTimeField(blank=True),
        ),
    ]