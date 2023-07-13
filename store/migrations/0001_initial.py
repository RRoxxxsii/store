# Generated by Django 4.2.2 on 2023-06-18 05:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('in_stock', models.BooleanField(default=False)),
                ('slug', models.SlugField()),
                ('image_url', models.ImageField(blank=True, default='media/images.png', null=True, upload_to='categories/uploads/%Y/%m/%d/')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='store.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.ImageField(blank=True, null=True, upload_to='products/uploads/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('logo_url', models.ImageField(blank=True, default='media/images.png', null=True, upload_to='logos/uploads/%Y/%m/%d/')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('discount_percent', models.IntegerField(max_length=2)),
                ('in_stock', models.BooleanField(default=True)),
                ('amount', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category')),
                ('image', models.ForeignKey(default='media/images.png', on_delete=django.db.models.deletion.SET_DEFAULT, to='store.productimage')),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.vendor')),
            ],
        ),
    ]
