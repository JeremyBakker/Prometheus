from django.conf.urls import url, include
from rest_framework import routers
from . import views
from django.contrib import admin

app_name = 'Prometheus'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
    url(r'^AAPL/$', views.AAPL_transcript, 
        name='AAPL'),
    url(r'^AMZN/$', views.AMZN_transcript, 
        name='AMZN'),
]
