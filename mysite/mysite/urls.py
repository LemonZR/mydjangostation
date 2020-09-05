"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from django.urls import include

from django.conf.urls.static import static

# from .settings import MEDIA_ROOT, MEDIA_URL

from django.urls import re_path
import re
from django.views.static import serve
from .views import index

# urlpatterns = [
#     path('polls/', include('polls.urls')),
#     path('admin/', admin.site.urls),
#     re_path(r'^%s(?P<path>.*)$' % re.escape(MEDIA_URL.lstrip('/')), serve, kwargs={'document_root': '%s' % MEDIA_ROOT}),
#
# ]
urlpatterns = [
    path('', index),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),

]  # + static(MEDIA_URL, document_root=MEDIA_ROOT)

# def my_static(prefix, view=serve, **kwargs):
#     """
#     Return a URL pattern for serving files in debug mode.
#
#     from django.conf import settings
#     from django.conf.urls.my_static import my_static
#
#     urlpatterns = [
#         # ... the rest of your URLconf goes here ...
#     ] + my_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     """
#     if not prefix:
#         raise ImproperlyConfigured("Empty my_static prefix not permitted")
#     elif not settings.DEBUG or urlsplit(prefix).netloc:
#         # No-op if not in debug mode or a non-local prefix.
#         return []
#     return [
#         re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
#     ]
