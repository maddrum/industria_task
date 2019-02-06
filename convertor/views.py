from django.views.generic import ListView, CreateView, UpdateView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.urls.exceptions import Http404
from .models import Currencies
from .forms import CurrencyFormClass, ConvertFormClass


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
