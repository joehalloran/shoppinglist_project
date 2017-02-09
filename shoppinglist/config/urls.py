"""shoppinglist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import urls
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

import oauth2client.contrib.django_util.site as django_util_site
from oauth2client.contrib.django_util import decorators

from core import views

urlpatterns = [
	url(r'^$', decorators.oauth_enabled(TemplateView.as_view(template_name='pages/home.html')), name='home'),
	url(r'^mylists/', include('lists.urls')),
    url(r'^admin/', admin.site.urls),
    # oAuth required views
    url(r'^oauth2/', include(django_util_site.urls)),
    url(r'^logout/$', views.logout, name='logout'),
]
