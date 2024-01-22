from django.db import models


class NetworkElement(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название звена')
    supplier = models.ForeignKey('self', null=True, blank=True, default=None, on_delete=models.SET_DEFAULT)
    level = models.IntegerField(default=0)
    debt_to_supplier = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                           verbose_name='Задолженность перед поставщиком')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    class Meta:
        verbose_name = 'Звено сети'
        verbose_name_plural = 'Звенья сети'


class Product(models.Model):
    network_element = models.ForeignKey(NetworkElement, on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=100, verbose_name='Название продукта')
    model = models.CharField(max_length=50, verbose_name='Модель')
    release_date = models.DateField(verbose_name='Дата выхода на рынок')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Contacts(models.Model):
    network_element = models.OneToOneField(NetworkElement, on_delete=models.CASCADE, blank=True, null=True)

    email = models.EmailField(verbose_name='Email')
    country = models.CharField(max_length=70, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'
        ordering = ['country']
