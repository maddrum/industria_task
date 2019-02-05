from django.conf.urls import url
from convertor import views

app_name = 'convertor'
urlpatterns = [
    url(r'^list/$', views.ListCurrencies.as_view(), name='list_currencies'),
    url(r'^create/$', views.AddCurrency.as_view(), name='create_currency'),
    url(r'convert/$', views.ConvertCurrencies.as_view(), name='currency_convertor'),
    url(r'^update-list/$', views.EditCurrencyListView.as_view(), name='update_list'),
    url(r'^update/(?P<pk>\d+)/$', views.EditCurrencyUpdateView.as_view(), name='update_currency'),
]
