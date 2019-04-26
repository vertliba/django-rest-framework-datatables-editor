from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers

from albums import views

# router = DatatablesDefaultRouter()
router = routers.DefaultRouter()
router.register(r'albums', views.AlbumViewSet)
router.register(r'artists', views.ArtistViewSet)


urlpatterns = [
    url('^admin/', admin.site.urls),
    url('^api/', include(router.urls)),
    url('^$', views.index, name='albums')
]
