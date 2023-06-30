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

    def save(self, *args, **kwargs):
        self.vendor_name = self.vendor_name.capitalize()
        super(Vendor, self).save(*args, **kwargs)


class Category(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Категория', unique=True)
    description = models.TextField(verbose_name='Описание')
    in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/uploads/%Y/%m/%d/', null=True, blank=True,
                              default='media/images.png', verbose_name='Изображение')

    parent = models.ForeignKey('self', on_delete=models.PROTECT, related_name='children', null=True, blank=True,
                               verbose_name='Родительская категория')

    is_parent_category = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.parent}, {self.category_name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        self.category_name = self.category_name.capitalize()
        super(Category, self).save(*args, **kwargs)


class Brand(models.Model):
    brand_name = models.CharField(verbose_name='Бренд', max_length=255, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'

    def save(self, *args, **kwargs):
        self.brand_name = self.brand_name.capitalize()
        super(Brand, self).save(*args, **kwargs)


class Product(models.Model):
    product_name = models.CharField(max_length=255, verbose_name='Товар')
    description = models.TextField(verbose_name='Описание')

    price = models.IntegerField(verbose_name='Цена')
    discount_percent = models.PositiveIntegerField(default=0, verbose_name='Процент скидки')

    in_stock = models.BooleanField(default=False, verbose_name='В наличии')
    amount = models.IntegerField(verbose_name='Количество')

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, verbose_name='Поставщик')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name='Бренд')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def get_price_with_discount(self):
        return int(self.price - self.price / 100 * self.discount_percent) if self.discount_percent > 0 else self.price

    def __str__(self):
        return f'{self.product_name} - {self.price} руб.'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['product_name', ]

    def save(self, *args, **kwargs):
        self.product_name = self.product_name.capitalize()
        super(Product, self).save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name="Изображение")

    alt_text = models.CharField(
        verbose_name="Альтернативый текст",
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Карточка товара'
        verbose_name_plural = 'Карточки товара'

    def __str__(self):
        return str(self.product)

