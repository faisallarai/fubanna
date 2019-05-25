from django.urls import path, re_path

from .views import (HomePageView, LogoutPageView, CustomUserListView, CustomUserDetailView,
                    RegisterView, ContactView, activate_view, LoginPageView,
                    UserActivationSentView)

app_name = 'main'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('accounts/', CustomUserListView.as_view(), name='accounts'),
    path('accounts/<int:pk>/', CustomUserDetailView.as_view(),
         name='accounts-detail'),
    path('user_activation_sent/', UserActivationSentView.as_view(),
         name='user_activation_sent'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            activate_view, name='activate'),
]
