# Generated by Django 4.2.2 on 2023-06-18 07:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_productimage_image_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=255, verbose_name='Бренд')),
                ('slug', models.SlugField()),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=255, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='category',
            name='image_url',
            field=models.ImageField(blank=True, default='media/images.png', null=True, upload_to='categories/uploads/%Y/%m/%d/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='category',
            name='in_stock',
            field=models.BooleanField(default=False, verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='store.category', verbose_name='Родительская категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='amount',
            field=models.IntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='discount_percent',
            field=models.IntegerField(default=0, verbose_name='Процент скидки'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ForeignKey(default='media/images.png', on_delete=django.db.models.deletion.SET_DEFAULT, to='store.productimage', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=True, verbose_name='В наличии'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=255, verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='product',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.vendor', verbose_name='Поставщик'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image_url',
            field=models.ImageField(blank=True, default='media/images.png', null=True, upload_to='products/uploads/%Y/%m/%d/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='logo_url',
            field=models.ImageField(blank=True, default='media/images.png', null=True, upload_to='logos/uploads/%Y/%m/%d/', verbose_name='Логотип'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_name',
            field=models.CharField(max_length=255, verbose_name='Поставщик'),
        ),
    ]
