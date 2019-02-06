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


class ConvertCurrencies(FormView):
    """Currency Convertor"""
    template_name = 'convertor/convertor.html'
    form_class = ConvertFormClass
    success_url = reverse_lazy('convertor:currency_convertor')

    def __init__(self, *args, **kwargs):
        super(ConvertCurrencies, self).__init__(*args, **kwargs)
        self.result = 0
        self.from_currency_code = ''
        self.to_currency_code = ''
        self.amount = 0

    def form_valid(self, form):
        from_currency = Currencies.objects.get(currency_code=form.cleaned_data['from_currency'])
        to_currency = Currencies.objects.get(currency_code=form.cleaned_data['to_currency'])
        self.from_currency_code = from_currency.currency_code
        self.to_currency_code = to_currency.currency_code
        self.amount = float(form.cleaned_data['amount'])
        from_lv = float(from_currency.exchange_rate) * float(self.amount) / from_currency.units
        print(from_lv)
        self.result = from_lv / float(to_currency.exchange_rate) * to_currency.units
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super(ConvertCurrencies, self).get_context_data(**kwargs)
        context['from'] = self.from_currency_code
        context['to'] = self.to_currency_code
        context['result'] = round(float(self.result), 2)
        context['amount'] = self.amount
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
