# Generated by Django 4.2.2 on 2023-06-19 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_alter_category_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='in_stock',
            field=models.BooleanField(default=False, verbose_name='В наличии'),
        ),
    ]