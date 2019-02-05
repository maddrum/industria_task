from django.db import models


class Currencies(models.Model):
    """Stores information for currency type and exchange rates to BGN"""
    currency_code = models.CharField(max_length=3, unique=True)
    exchange_rate = models.DecimalField(max_digits=19, decimal_places=2)
    created_on = models.DateTimeField(auto_now=True)
    edited_on = models.DateTimeField(auto_now_add=True)
