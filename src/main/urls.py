from django.urls import path

from .views import (HomePageView, ContactPageView)

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('contact/', ContactPageView.as_view(), name='contact'),
]
