from django.urls import path

from .views import (LogoutPageView, AgentDetailView,
                    RegisterView, LoginPageView, send_login_email, activate_login_email,
                    UserActivationSentView)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('send_email/', send_login_email, name='send_login_email'),
    path('activate_email/<uuid:uid>/', activate_login_email, name='activate'),
    path('logout/', LogoutPageView.as_view(), name='logout'),
    path('agents/<slug:slug>/', AgentDetailView.as_view(), name='profile'),
    path('user_activation_sent/', UserActivationSentView.as_view(),
         name='user_activation_sent')
]
