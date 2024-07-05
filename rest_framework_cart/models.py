from django.db import models


class AbstractProduct(models.Model):
    title = models.CharField(max_length=255, default=None, verbose_name='Product title')
    price = models.DecimalField(decimal_places=2, default=0, verbose_name='Product price')

    class Meta:
        abstract = True
