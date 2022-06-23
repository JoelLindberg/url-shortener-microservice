from django.urls import path

from . import views

urlpatterns = [
    path('developer/<slug:slug>', views.developer, name='developer'),
    path('shorturl', views.url_shortener, name='url_shortener'),
    path('shorturl/<slug:id>', views.short_url_redirect, name='short_url_redirect')
]