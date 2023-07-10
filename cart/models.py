import uuid

from django.db import models

from account.models import Customer
from store.models import Product


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)

    owner = models.OneToOneField(Customer, verbose_name='Владелец корзины', on_delete=models.CASCADE,
                                 null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100)
    completed = models.BooleanField(default=False, verbose_name='Заполнено')

    def __str__(self):
        return f'ID: {self.id}, Владелец: {self.owner}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", null=True,
                             blank=True, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems',
                                verbose_name='Товар')
    amount = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return f'Корзина: {self.cart}, товар: {self.product}'
