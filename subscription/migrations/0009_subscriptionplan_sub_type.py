# Generated by Django 4.2.7 on 2023-12-07 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_alter_subscription_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='sub_type',
            field=models.CharField(choices=[('BS', 'Basic'), ('PR', 'Premium')], default='BS', max_length=2),
            preserve_default=False,
        ),
    ]
