# Generated by Django 4.2.2 on 2023-06-18 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(default=0),
        ),
    ]
