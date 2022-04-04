from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from django import forms



class Profile(models.Model):
    """
    Профиль пользователя. Если баданс <= 0 он не сможет покупать.
    Статус зависит от суммы покупок.
    """
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    balance = models.IntegerField(default=0)
    status = models.IntegerField(default=0)


class Product(models.Model):
    """
    Модель товара
    """
    title = models.CharField(max_length=200, default='', verbose_name='название')
    description = models.CharField(max_length=1000, default='', verbose_name='описание')
    market = models.CharField(max_length=200, default='', verbose_name='магазин')
    price = models.IntegerField(default=0, verbose_name='цена')
    rate = models.IntegerField(default=0, verbose_name='рейтинг')

    def __str__(self):
        return self.title


class Cart(models.Model):
    """
    Модель корзины для данного юзера
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)


class CartItem(models.Model):
    """
    Товар в корзине
    """
    product = models.ForeignKey(Product, default='', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    cart = models.ForeignKey(Cart, default='', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
