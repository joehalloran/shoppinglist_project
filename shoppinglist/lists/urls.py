from django.conf.urls import url

from . import views

app_name = 'lists'
urlpatterns = [
    url(r'^$', views.MyListView.as_view(), name='mylists'),
    url(r'^edit/(?P<pk>[0-9]+)/$', views.editListView, name='edit'),
    url(r'^create/$', views.ListCreate.as_view(), name='create'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.ListDelete.as_view(), name='delete'),
]
