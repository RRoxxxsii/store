# Generated by Django 4.2.2 on 2023-06-10 10:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_emailconfirmationtoken'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailconfirmationtoken',
            name='customer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]