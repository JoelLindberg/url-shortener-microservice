from django.urls import path

from . import views

urlpatterns = [
    path('/<slug:slug>', views.url_shortener, name='url_shortener')
]