from django.views.generic import ListView, CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls.exceptions import Http404
from xml_parser import get_currency_values
from .models import Currencies
from .forms import CurrencyFormClass


class IndexPage(TemplateView):
    """index page"""
    template_name = 'convertor/index.html'


class ListCurrencies(ListView):
    """Lists all currencies"""
    model = Currencies
    template_name = 'convertor/list.html'


class ConvertCurrencies(TemplateView):
    """Currency Convertor"""
    template_name = 'convertor/convertor.html'

    def get_context_data(self, **kwargs):
        context = super(ConvertCurrencies, self).get_context_data(**kwargs)
        all_currencies = Currencies.objects.all()
        all_currencies_list = [item.currency_code for item in all_currencies]
        exchange_rates = {item.currency_code: item.exchange_rate for item in all_currencies}
        exchange_units = {item.currency_code: item.units for item in all_currencies}
        context['exchange_rates'] = exchange_rates
        context['exchange_units'] = exchange_units
        context['all_currencies'] = all_currencies_list
        return context


class AddCurrency(LoginRequiredMixin, CreateView):
    """Adds New Currency If You Are Admin"""
    model = Currencies
    form_class = CurrencyFormClass
    template_name = 'convertor/input_form.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(AddCurrency, self).dispatch(request, *args, **kwargs)


class EditCurrencyListView(LoginRequiredMixin, ListView):
    """Shows List of All Currencies Added"""
    model = Currencies
    template_name = 'convertor/list_update.html'


class EditCurrencyUpdateView(LoginRequiredMixin, UpdateView):
    """Manually Edit Currency"""
    model = Currencies
    form_class = CurrencyFormClass
    template_name = 'convertor/update_form.html'
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        return super(EditCurrencyUpdateView, self).dispatch(request, *args, **kwargs)


class AutoUpdateCurrencies(ListView):
    model = Currencies
    template_name = 'convertor/list_autoupdate.html'

    def auto_update(self):
        """Auto updates all currencies"""
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
            currency.save()

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404()
        self.auto_update()
        return super(AutoUpdateCurrencies, self).dispatch(request, *args, **kwargs)
