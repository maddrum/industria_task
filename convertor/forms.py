from django import forms
from .models import Currencies


class CurrencyFormClass(forms.ModelForm):
    """A Model Class For Currencies"""

    class Meta:
        model = Currencies
        fields = ('currency_code', 'exchange_rate', 'units')


class ConvertFormClass(forms.Form):
    """Convertor form"""
    all_currencies = [((item.currency_code), (item.currency_code)) for item in Currencies.objects.all()]
    amount = forms.DecimalField(max_digits=19, decimal_places=2)
    from_currency = forms.ChoiceField(choices=all_currencies)
    to_currency = forms.ChoiceField(choices=all_currencies)
