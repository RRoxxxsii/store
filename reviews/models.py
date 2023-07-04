from django.db import models

from account.models import Customer
from store.models import Product


class ProductReview(models.Model):
    LESS_THAN_MONTH = 'LESS THAN MONTH'
    MONTH_TO_YEAR_HALF = 'MONTH_TO_YEAR_HALF'
    YEAR_HALF_TO_ONE_YEAR = 'YEAR_HALF_TO_ONE_YEAR'
    ONE_YEAR_MORE = 'ONE_YEAR_MORE'

    CHOICES = (
        (LESS_THAN_MONTH, 'Меньше месяца'),
        (MONTH_TO_YEAR_HALF, 'От месяца до полугода'),
        (YEAR_HALF_TO_ONE_YEAR, 'От полугода до года'),
        (ONE_YEAR_MORE, 'Более одного года')
    )

    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    user = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')

    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='Рейтинг')
    usage_period = models.CharField(max_length=255, choices=CHOICES, verbose_name='Срок использования')
    advantages = models.TextField(verbose_name='Преимущества')
    disadvantages = models.TextField(verbose_name='Недостатки')

    comment = models.TextField(verbose_name='Комментарий')

    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-created',]



