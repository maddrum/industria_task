from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from convertor.views import IndexPage

urlpatterns = [
    url(r'^$', IndexPage.as_view(), name='index'),
    url(r'^convertor/', include('convertor.urls', namespace='convertor')),
    path('admin/', admin.site.urls),

]
