from django import forms
from .models import Currencies


class CurrencyFormClass(forms.ModelForm):
    """A Model Class For Currencies"""

    class Meta:
        model = Currencies
        fields = ('currency_code', 'exchange_rate')
