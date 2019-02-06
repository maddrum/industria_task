from django.core.management.base import BaseCommand
from convertor.models import Currencies
from xml_parser import get_currency_values


class Command(BaseCommand):
    def handle(self, *args, **options):
        updated_currencies = get_currency_values()
        all_objects = Currencies.objects.all()
        for currency in all_objects:
            if currency.currency_code == "EUR":
                currency.units = 1
                currency.exchange_rate = 1.9558
                currency.save()
                continue
            if currency.currency_code == "BGN":
                currency.units = 1
                currency.exchange_rate = 1.00
                currency.save()
                continue
            new_rate = updated_currencies.get(currency.currency_code)
            if new_rate is not None:
                currency.exchange_rate = new_rate['rate']
                currency.units = new_rate['units']
            else:
                print(f'Currency named: {currency.currency_code} was not found in BNB site. Ignored!')
            currency.save()
