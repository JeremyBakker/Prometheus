from django.conf.urls import url, include
from rest_framework import routers
from . import views
from django.contrib import admin

router = routers.DefaultRouter()
router.register(r'transcript', views.TranscriptViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index'),
]
