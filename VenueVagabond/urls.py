"""VenueVagabond URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.conf.urls import include
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from vvAPI.views import StateView, register_user, login_user, EventTypeView, EventView, VenueView, EventImageView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'states', StateView, 'state')
router.register(r'eventtypes', EventTypeView, 'eventtype')
router.register(r'events', EventView, 'event')
router.register(r'venues', VenueView, 'venue')
router.register(r'eventimages', EventImageView, 'eventimage')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
