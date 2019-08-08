from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^travel', views.travel),
    url(r'^addtrip', views.addtrip),
    url(r'^savetrip', views.savetrip),
    url(r'^viewtrip', views.viewtrip),
    url(r'^deletetrip', views.deletetrip),
    url(r'^canceltrip', views.canceltrip),
    url(r'^jointrip', views.jointrip),
]
