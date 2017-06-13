from django.conf.urls import url, include
from rest_framework import routers
from . import views
from django.contrib import admin

app_name = 'Prometheus'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
    url(r'^AAPL/$', views.transcript, 
        name='AAPL'),
    url(r'^AMZN/$', views.transcript, 
        name='AMZN'),
    url(r'^ADBE/$', views.transcript, 
        name='ADBE'),
    url(r'^HPQ/$', views.transcript, 
        name='HPQ'),
    url(r'^IBM/$', views.transcript, 
            name='IBM'),
    url(r'^MSFT/$', views.transcript, 
            name='MSFT'),
    url(r'^ORCL/$', views.transcript, 
            name='ORCL'),
    url(r'^KRX005930/$', views.transcript, 
                name='KRX005930'),
    url(r'^search/$', views.search, name='search')
]
