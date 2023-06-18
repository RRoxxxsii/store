from django.db import models


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=255, verbose_name='Поставщик')
    description = models.TextField(verbose_name='Описание')
    logo_url = models.ImageField(upload_to='logos/uploads/%Y/%m/%d/', null=True, blank=True,
                                 default='media/images.png', verbose_name='Логотип')

    def __str__(self):
        return self.vendor_name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Категория')
    description = models.TextField(verbose_name='Описание')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    slug = models.SlugField()
    image_url = models.ImageField(upload_to='categories/uploads/%Y/%m/%d/', null=True, blank=True,
                                  default='media/images.png', verbose_name='Изображение')

    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', null=True, blank=True,
                               verbose_name='Родительская категория')

    def __str__(self):
        return f'{self.parent}, {self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class ProductImage(models.Model):
    image_url = models.ImageField(upload_to='products/uploads/%Y/%m/%d/', null=True, blank=True,
                                  default='media/images.png', verbose_name='Изображение')

    class Meta:
        verbose_name = 'Карточка товара'
        verbose_name_plural = 'Карточки товара'


class Brand(models.Model):
    brand_name = models.CharField(verbose_name='Бренд', max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name='Товар')
    description = models.TextField(verbose_name='Описание')

    price = models.IntegerField(verbose_name='Цена')
    discount_percent = models.IntegerField(default=0, verbose_name='Процент скидки')

    in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    amount = models.IntegerField(verbose_name='Количество')

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Поставщик')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд')
    image = models.ForeignKey(ProductImage, on_delete=models.SET_DEFAULT, default='media/images.png',
                              verbose_name='Изображение')

    def get_price_with_discount(self):
        return self.price - self.price / self.discount_percent

    def __str__(self):
        return f'{self.product_name} - {self.price} руб.'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


